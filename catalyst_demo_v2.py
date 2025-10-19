#!/usr/bin/env python3
"""
The Catalyst - Demo Pipeline
Processes video/audio Sparks through transcription and LLM analysis

Flow: Video → faster-whisper → transcript → Ollama/Mistral → structured analysis → Obsidian notes
"""

import os
import re
import json
import time
from pathlib import Path
from datetime import datetime
import subprocess
import requests
from faster_whisper import WhisperModel

# ============================================================================
# CONFIGURATION - Edit these to match your setup
# ============================================================================

# Where your Spark videos live
INPUT_DIR = "/mnt/z/Sparks"

# Where output markdown files will go
OUTPUT_DIR = "/mnt/z/Catalyst-Demo"

# Your FastAPI endpoint on wcn-oglaptop
OLLAMA_ENDPOINT = "http://wcn-oglaptop:8000/api/review"

# How many Sparks to process (start small for testing)
MAX_SPARKS = 10

# Enable debug output for troubleshooting
DEBUG_MODE = True

# Whisper model size (tiny, base, small, medium, large-v2)
# "base" is fast and good enough for demo
WHISPER_MODEL = "base"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_spark_filename(filename):
    """
    Extract timestamp from filename like 'Replay 2025-09-29 16-05-04.mp4'
    Returns: datetime object or None
    """
    # Pattern: "Replay YYYY-MM-DD HH-MM-SS"
    pattern = r'Replay (\d{4})-(\d{2})-(\d{2}) (\d{2})-(\d{2})-(\d{2})'
    match = re.search(pattern, filename)
    
    if match:
        year, month, day, hour, minute, second = match.groups()
        return datetime(int(year), int(month), int(day), 
                       int(hour), int(minute), int(second))
    
    # Fallback: try to parse any date in filename
    # You can add more patterns here if your filenames vary
    return None


def get_video_duration(filepath):
    """
    Get video duration using ffprobe
    Returns: duration in seconds (float) or None
    """
    try:
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(filepath)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return float(result.stdout.strip())
    except:
        return None


def transcribe_spark(filepath, model):
    """
    Use faster-whisper to transcribe audio/video
    Returns: transcript text (string)
    """
    print(f"  🎤 Transcribing with faster-whisper...")
    
    # Transcribe with word-level timestamps
    segments, info = model.transcribe(
        str(filepath),
        beam_size=5,
        language="en",  # Force English, or use None for auto-detect
        word_timestamps=True
    )
    
    # Combine all segments into full transcript
    transcript = " ".join([segment.text.strip() for segment in segments])
    
    print(f"  ✓ Transcription complete ({len(transcript)} chars)")
    return transcript


def analyze_with_mistral(transcript, retry_count=3, debug=False):
    """
    Send transcript to Ollama via FastAPI for LLM analysis
    Returns: analysis dict or None if failed
    
    Uses exponential backoff retry logic for connection issues
    """
    print(f"  🧠 Analyzing with Mistral...")
    
    # Build the prompt for structured analysis
    prompt = f"""Analyze this personal development voice note according to the Evolutions Methodology.

VOICE NOTE TRANSCRIPT:
{transcript}

ANALYSIS FRAMEWORK:
- Categories: methodology, product-strategy, fitness, mental-health, technical, business
- Evolution Phase: Which part of the system is being developed (catalyst, spark-app, clipboard, ditl)
- Insight Type: connection, obstacle, decision, question, breakthrough, reflection
- Energy Level: high, medium, low, frustrated, excited, contemplative
- Actionable: Does this contain a specific task or decision? (true/false)
- Key Concepts: Extract 3-5 main concepts or terms mentioned

Respond ONLY with valid JSON in this exact format:
{{
    "category": ["list", "of", "categories"],
    "evolution_phase": "phase-name",
    "insight_type": "type",
    "energy": "level",
    "actionable": true,
    "key_concepts": ["concept1", "concept2", "concept3"],
    "summary": "One sentence summary of the core insight",
    "methodology_alignment": "How this relates to Evolutions framework"
}}"""

    # Retry logic with exponential backoff (from your existing code)
    for attempt in range(retry_count):
        try:
            response = requests.post(
                OLLAMA_ENDPOINT,
                json={
                    "text": prompt,
                    "model": "mistral"
                },
                timeout=60  # 60 second timeout per request
            )
            
            if debug:
                print(f"\n  [DEBUG] Status Code: {response.status_code}")
                print(f"  [DEBUG] Raw response: {response.text[:500]}")
            
            if response.status_code == 200:
                result = response.json()
                
                # Try to parse the LLM response as JSON
                # Mistral sometimes wraps JSON in markdown code blocks
                llm_output = result.get('response', result.get('text', ''))
                
                if debug:
                    print(f"  [DEBUG] LLM output (first 500 chars): {llm_output[:500]}")
                
                # Strip markdown code blocks if present
                llm_output = re.sub(r'^```json\s*', '', llm_output)
                llm_output = re.sub(r'\s*```$', '', llm_output)
                llm_output = llm_output.strip()
                
                analysis = json.loads(llm_output)
                print(f"  ✓ Analysis complete")
                return analysis
            
            else:
                print(f"  ⚠ Attempt {attempt+1} failed: HTTP {response.status_code}")
                if debug:
                    print(f"  [DEBUG] Response body: {response.text}")
                
        except json.JSONDecodeError as e:
            print(f"  ⚠ Attempt {attempt+1} failed: Invalid JSON - {str(e)}")
            if debug:
                print(f"  [DEBUG] Attempted to parse: {llm_output[:500] if 'llm_output' in locals() else 'N/A'}")
        except Exception as e:
            print(f"  ⚠ Attempt {attempt+1} failed: {str(e)}")
        
        # Wait before retry (exponential backoff: 1s, 2s, 4s)
        if attempt < retry_count - 1:
            wait_time = 2 ** attempt
            print(f"  ⏳ Waiting {wait_time}s before retry...")
            time.sleep(wait_time)
    
    print(f"  ❌ Analysis failed after {retry_count} attempts")
    return None


def generate_spark_markdown(spark_data, output_dir):
    """
    Generate individual Spark markdown file with YAML frontmatter
    """
    # Create safe filename from timestamp
    timestamp = spark_data['timestamp']
    filename = f"spark-{timestamp.strftime('%Y-%m-%d-%H-%M-%S')}.md"
    filepath = output_dir / "Sparks" / filename
    
    # Build YAML frontmatter
    frontmatter = f"""---
timestamp: {timestamp.isoformat()}
duration: {spark_data['duration']:.1f}s
spark_id: {spark_data['spark_id']}
original_file: {spark_data['original_filename']}
category: {json.dumps(spark_data['analysis'].get('category', []))}
evolution_phase: {spark_data['analysis'].get('evolution_phase', 'unknown')}
insight_type: {spark_data['analysis'].get('insight_type', 'unknown')}
energy: {spark_data['analysis'].get('energy', 'unknown')}
actionable: {str(spark_data['analysis'].get('actionable', False)).lower()}
key_concepts: {json.dumps(spark_data['analysis'].get('key_concepts', []))}
---

# Spark: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}

## Transcript

{spark_data['transcript']}

## Analysis

**Summary**: {spark_data['analysis'].get('summary', 'No summary available')}

**Methodology Alignment**: {spark_data['analysis'].get('methodology_alignment', 'Not analyzed')}

**Key Concepts**: {', '.join(spark_data['analysis'].get('key_concepts', []))}

---

*Generated by The Catalyst Demo*
"""
    
    # Write file
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(frontmatter)
    print(f"  📝 Written: {filename}")


def generate_index_report(all_sparks, output_dir):
    """
    Generate main index.md with Dataview queries and summary stats
    """
    # Calculate summary stats
    total_sparks = len(all_sparks)
    total_duration = sum(s['duration'] for s in all_sparks)
    
    # Count by category (flatten lists)
    all_categories = []
    for s in all_sparks:
        all_categories.extend(s['analysis'].get('category', []))
    category_counts = {}
    for cat in all_categories:
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    # Count by insight type
    insight_counts = {}
    for s in all_sparks:
        insight = s['analysis'].get('insight_type', 'unknown')
        insight_counts[insight] = insight_counts.get(insight, 0) + 1
    
    # Build report
    report = f"""# The Catalyst Demo Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary Statistics

- **Total Sparks Analyzed**: {total_sparks}
- **Total Duration**: {total_duration/60:.1f} minutes
- **Average Spark Length**: {total_duration/total_sparks:.1f} seconds

### Category Breakdown

"""
    
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_sparks) * 100
        report += f"- **{cat}**: {count} ({percentage:.1f}%)\n"
    
    report += f"""

### Insight Types

"""
    
    for insight, count in sorted(insight_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_sparks) * 100
        report += f"- **{insight}**: {count} ({percentage:.1f}%)\n"
    
    # Add Dataview table query
    report += f"""

---

## All Sparks (Dataview Table)

```dataview
TABLE 
    timestamp as "Time",
    duration as "Duration",
    insight_type as "Type",
    energy as "Energy",
    category as "Categories"
FROM "Catalyst-Demo/Sparks"
SORT timestamp DESC
```

---

## High-Energy Breakthroughs

```dataview
TABLE 
    timestamp as "Time",
    key_concepts as "Concepts",
    file.link as "Spark"
FROM "Catalyst-Demo/Sparks"
WHERE energy = "high" OR energy = "excited"
AND insight_type = "breakthrough"
SORT timestamp DESC
```

---

## Actionable Items

```dataview
TABLE 
    timestamp as "Time",
    insight_type as "Type",
    file.link as "Spark"
FROM "Catalyst-Demo/Sparks"
WHERE actionable = true
SORT timestamp DESC
```

---

## Category: Methodology Development

```dataview
LIST
FROM "Catalyst-Demo/Sparks"
WHERE contains(category, "methodology")
SORT timestamp DESC
```

---

## Recent Obstacles

```dataview
TABLE
    timestamp as "When",
    energy as "Energy",
    file.link as "Details"
FROM "Catalyst-Demo/Sparks"
WHERE insight_type = "obstacle"
SORT timestamp DESC
LIMIT 10
```

---

*Generated by The Catalyst - Demo Pipeline*
*Purpose: Prove transcription → inference → intelligence extraction*
"""
    
    # Write index
    filepath = output_dir / "index.md"
    filepath.write_text(report)
    print(f"\n📊 Index report written: {filepath}")


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def main():
    print("=" * 70)
    print("THE CATALYST - Demo Pipeline")
    print("=" * 70)
    print()
    
    # Validate input directory
    input_path = Path(INPUT_DIR)
    if not input_path.exists():
        print(f"❌ ERROR: Input directory not found: {INPUT_DIR}")
        return
    
    # Create output directory
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"📁 Input: {INPUT_DIR}")
    print(f"📁 Output: {OUTPUT_DIR}")
    print()
    
    # Find Spark files (video/audio)
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.m4a', '.mp3', '.wav'}
    spark_files = [f for f in input_path.iterdir() 
                   if f.suffix.lower() in video_extensions]
    
    # Limit for testing
    spark_files = spark_files[:MAX_SPARKS]
    
    print(f"🎯 Found {len(spark_files)} Spark files to process")
    print()
    
    # Initialize Whisper model (this loads once, then reuses)
    print("🔧 Loading Whisper model...")
    whisper_model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
    print("✓ Whisper model loaded")
    print()
    
    # Process each Spark
    all_sparks = []
    
    for i, spark_file in enumerate(spark_files, 1):
        print(f"[{i}/{len(spark_files)}] Processing: {spark_file.name}")
        print("-" * 70)
        
        # Extract metadata
        timestamp = parse_spark_filename(spark_file.name)
        if not timestamp:
            print(f"  ⚠ Could not parse timestamp from filename, using file mtime")
            timestamp = datetime.fromtimestamp(spark_file.stat().st_mtime)
        
        duration = get_video_duration(spark_file)
        if not duration:
            print(f"  ⚠ Could not get duration, estimating 60s")
            duration = 60.0
        
        print(f"  📅 Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  ⏱️  Duration: {duration:.1f}s")
        
        # Transcribe
        transcript = transcribe_spark(spark_file, whisper_model)
        
        # Analyze with LLM
        analysis = analyze_with_mistral(transcript, debug=DEBUG_MODE)
        
        if not analysis:
            print(f"  ⚠ Skipping this Spark due to analysis failure")
            print()
            continue
        
        # Store data
        spark_data = {
            'timestamp': timestamp,
            'duration': duration,
            'spark_id': spark_file.stem.lower().replace(' ', '-'),
            'original_filename': spark_file.name,
            'transcript': transcript,
            'analysis': analysis
        }
        
        # Generate individual markdown file
        generate_spark_markdown(spark_data, output_path)
        
        # Add to collection
        all_sparks.append(spark_data)
        
        print()
    
    # Generate index report
    if all_sparks:
        print("=" * 70)
        print("Generating index report...")
        generate_index_report(all_sparks, output_path)
        print()
        print("=" * 70)
        print(f"✨ COMPLETE! Processed {len(all_sparks)} Sparks")
        print(f"📂 View results in: {OUTPUT_DIR}")
        print("=" * 70)
    else:
        print("❌ No Sparks were successfully processed")


if __name__ == "__main__":
    main()
