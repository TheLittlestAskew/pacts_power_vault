// 💾 Save to GitHub: taylorritchie/claude-artifacts/javascript/2026-05-16_pp-transcribe.js
/**
 * ============================================================
 * Pacts & Power AssemblyAI Transcriber
 * ============================================================
 *
 * Transcribes Pacts & Power D&D session recordings using
 * AssemblyAI with campaign-specific vocabulary boosting and
 * custom spelling corrections pre-loaded from the campaign
 * spelling dictionary.
 *
 * LOCATION:
 *   C:\Users\theli\pacts_power_vault\Workflows\pp_transcribe\pp_transcribe.js
 *
 * PREREQUISITES:
 *   1. Node.js installed (v18+)
 *   2. AssemblyAI API key (https://www.assemblyai.com/app/account)
 *   3. Set your key in .env at the Workflows folder: ASSEMBLYAI_API_KEY=your_key
 *   4. npm install dotenv (from the Workflows folder)
 *   5. Session recordings in: pacts_power_vault\Session_Sources\Recordings\
 *
 * USAGE:
 *   cd C:\Users\theli\pacts_power_vault\Workflows\pp_transcribe
 *   node pp_transcribe.js                          (interactive picker)
 *   node pp_transcribe.js session13.mp3             (by filename)
 *   node pp_transcribe.js "C:\path\to\audio.mp3"   (full path)
 *
 * SUPPORTED FORMATS: mp3, mp4, m4a, wav, webm, ogg, flac
 * ============================================================
 */

const fs = require("fs");
const path = require("path");

// ── Load .env from the same folder as this script ───────────
const dotenvPath = path.resolve(__dirname, '.env');
require('dotenv').config({ path: dotenvPath });

// ── CONFIG ──────────────────────────────────────────────────
const API_KEY = process.env.ASSEMBLYAI_API_KEY;
const BASE_URL = "https://api.assemblyai.com";

if (!API_KEY) {
  console.error('ERROR: Missing ASSEMBLYAI_API_KEY.');
  console.error('Make sure .env exists in the Workflows folder with the key set.');
  process.exit(1);
}

// Default directories — all paths relative to the pacts_power_vault
const VAULT_ROOT = String.raw`C:\Users\theli\pacts_power_vault`;
const SCRIPT_DIR = path.join(VAULT_ROOT, "Workflows");
const RECORDINGS_DIR = path.join(VAULT_ROOT, "Session_Sources", "Recordings");
const TRANSCRIPTS_DIR = path.join(VAULT_ROOT, "Session_Sources", "Transcripts", "Raw_Unedited");

// Audio file extensions to look for when listing recordings
const AUDIO_EXTENSIONS = [".mp3", ".mp4", ".m4a", ".wav", ".webm", ".ogg", ".flac"];


// ══════════════════════════════════════════════════════════════
// PACTS & POWER CAMPAIGN VOCABULARY
// ══════════════════════════════════════════════════════════════
// These are the words/phrases AssemblyAI should prioritize
// recognizing. Up to 1,000 terms for Universal-3 Pro.
//
// Organized by category for easy maintenance.
// Add new terms as the campaign progresses.

const PP_KEYTERMS = [

  // ── Player Characters ──
  "Orphea Levistus",
  "Orphie",
  "Orphea",
  "Rinestra Genleth",
  "Rin",
  "Sanis Reylana",
  "Sanis",
  "Varis Aestra",
  "Varis",
  "Ogre",

  // ── Former / Inactive PCs ──
  "Lance Filo",
  "Braun",

  // ── Player Names (OOC) ──
  "Taylor",
  "Chet",
  "Rachel",
  "Gabe",
  "Vincent",
  "Chris",

  // ── DM / Table ──
  "heavyhart",

  // ── Recurring NPCs ──
  "Clarissa",
  "Selena",
  "Scrappy",
  "Pippi",
  "Hikara",

  // ── Ghost Mind Entities ──
  "Ghost Mind",
  "Eleni",
  "Gavril",
  "Vula",
  "Sarin",
  "The Whisper Mask",
  "The Veil",

  // ── Planeswalkers & MTG Canon Characters ──
  "Jace Beleren",
  "Jace",
  "Nicol Bolas",
  "Niv-Mizzet",
  "Vraska",
  "Ral Zarek",
  "Ral",
  "Chandra Nalaar",
  "Chandra",
  "Liliana Vess",
  "Liliana",
  "Professor Onyx",
  "Dovin Baan",
  "Domri Rade",
  "Ajani Goldmane",
  "Ajani",
  "Ugin",
  "Tezzeret",
  "Kaya Cassir",
  "Kaya",
  "Szadek",
  "Narset",
  "Nissa Revane",
  "Nissa",
  "Gideon Jura",
  "Gideon",
  "Sorin Markov",
  "Sorin",
  "Nahiri",

  // ── Ravnica Guilds (all 10) ──
  "Azorius Senate",
  "Azorius",
  "Boros Legion",
  "Boros",
  "Cult of Rakdos",
  "Rakdos",
  "Golgari Swarm",
  "Golgari",
  "Gruul Clans",
  "Gruul",
  "House Dimir",
  "Dimir",
  "Izzet League",
  "Izzet",
  "Orzhov Syndicate",
  "Orzhov",
  "Selesnya Conclave",
  "Selesnya",
  "Simic Combine",
  "Simic",

  // ── Ravnica Locations ──
  "Ravnica",
  "Tenth District",
  "New Prahv",
  "Sunhome",
  "Nivix",
  "Skarrg",
  "Vitu-Ghazi",
  "Orzhova",
  "Rix Maadi",
  "Zonot",
  "Precinct One",
  "Precinct Two",
  "Precinct Three",
  "Precinct Four",
  "Precinct Five",
  "Precinct Six",
  "The Rubblebelt",
  "Rubblebelt",
  "Transguild Promenade",
  "Plaza of Harmony",
  "Chamber of the Guildpact",
  "Undercity",

  // ── MTG Planes Visited ──
  "Amonkhet",
  "Ixalan",
  "Tarkir",
  "Dominaria",
  "Strixhaven",
  "Arcavios",
  "Theros",
  "Innistrad",
  "Zendikar",

  // ── Campaign Artifacts & Items ──
  "Leather Daddy Game Boy",
  "Leather Daddy Ball",
  "Blazebringer",
  "Sole Integrated Storage",
  "Dragon Spirit Box",
  "Immortal Sun",
  "Guildpact",
  "Living Guildpact",
  "Implicit Maze",

  // ── Campaign Factions & Groups ──
  "The Breakfast Club",
  "Gatewatch",
  "Eternals",
  "The Second Sun",
  "Boros Academy",

  // ── Creatures & Entities ──
  "Eternal",
  "Eternals",
  "Nephilim",
  "Wurm",
  "Angel",
  "Demon",
  "Sphinx",
  "Drake",

  // ── Ixalan NPCs & Terms ──
  "Kumena",
  "Mavren Fein",
  "Elenda",
  "Huatli",
  "Angrath",
  "Orazca",
  "Matzalantli",
  "Ghalta",
  "Etali",
  "Zetalpa",
  "Zacama",
  "Spitfire Bastion",

  // ── Tarkir NPCs & Terms ──
  "Chiso Zennar",
  "Sage-Eye Stronghold",
  "Zhiming Toshokan",
  "Lian Mei",
  "Renji",
  "Mardu Horde",
  "Merrevia Sal",
  "Jeskai",
  "Sultai",
  "Abzan",
  "Temur",
  "Mardu",

  // ── D&D Spells (commonly used by party) ──
  "Rage",
  "Reckless Attack",
  "Spirit Shield",
  "Ancestral Protectors",
  "Totem Spirit",
  "Danger Sense",
  "Feral Instinct",
  "Healing Word",
  "Guiding Bolt",
  "Sacred Flame",
  "Spirit Guardians",
  "Beacon of Hope",
  "Revivify",
  "Cure Wounds",
  "Shield of Faith",
  "Bless",
  "Spiritual Weapon",
  "Dispel Magic",
  "Eldritch Blast",
  "Hex",
  "Armor of Agathys",
  "Counterspell",
  "Hellish Rebuke",
  "Misty Step",
  "Hunter's Mark",
  "Cure Wounds",
  "Ensnaring Strike",
  "Charm Person",
  "Misty Wanderer",
  "Summon Fey",
  "Fire Bolt",
  "Chromatic Orb",
  "Fireball",
  "Lightning Bolt",
  "Shield",
  "Mage Armor",
  "Scorching Ray",
  "Haste",
  "Fly",
  "Hold Person",
  "Detect Magic",
  "Prestidigitation",
  "Thaumaturgy",

  // ── D&D Mechanics ──
  "Path of the Totem Warrior",
  "Light Domain",
  "Fey Wanderer",
  "Draconic Bloodline",
  "multiclass",
  "short rest",
  "long rest",
  "death save",
  "death saves",
  "opportunity attack",
  "saving throw",
  "ability check",
  "initiative",
  "darkvision",
  "cantrip",
  "concentration",
  "attunement",
  "proficiency",
  "disadvantage",
  "advantage",
  "Sneak Attack",
  "Bardic Inspiration",
  "Metamagic",
  "Wild Magic",
  "Extra Attack",
  "Brutal Critical",

  // ── Races ──
  "tiefling",
  "aasimar",
  "halfling",
  "dragonborn",
  "drow",
  "dark elf",
  "genasi",

  // ── D&D Terms ──
  "Planeswalker",
  "Leyline",
  "Parun",
  "Ecumenopolis",

  // ── Ogre's Traveling Tavern ──
  "Ogre's Traveling Tavern",
];


// ══════════════════════════════════════════════════════════════
// CUSTOM SPELLING CORRECTIONS
// ══════════════════════════════════════════════════════════════
// These fix AFTER transcription — replacing common misheard
// versions with the correct spelling.
//
// Format: { "to": "CorrectSpelling", "from": ["misheard1", "misheard2"] }
// The "from" values are case-insensitive.
//
// IMPORTANT: AssemblyAI requires 'to' values to be ONE word only.
// Multi-word corrections (e.g., "Nicol Bolas", "Ral Zarek") are
// handled by keyterms_prompt instead, which boosts recognition
// of the correct multi-word phrase during transcription.

const PP_CUSTOM_SPELLING = [

  // ── Player Characters ──
  { from: ["Orphy", "Orfie", "Orphi", "Orphieus", "Orphiea"], to: "Orphie" },
  { from: ["Ren", "Ryn", "Wren", "Rinistra"], to: "Rin" },
  { from: ["Santa", "Santis", "Santus", "Sanas", "Sannis", "Zannis"], to: "Sanis" },
  { from: ["Varys", "Varus"], to: "Varis" },
  { from: ["Ogur", "Oger"], to: "Ogre" },
  { from: ["Lantz"], to: "Lance" },
  { from: ["Brown", "Brawn"], to: "Braun" },
  { from: ["Clarisa"], to: "Clarissa" },
  { from: ["Selina", "Salena", "Celena"], to: "Selena" },

  // ── Planeswalkers & Canon Characters ──
  { from: ["Nicobolus", "Nicolas", "Nikolaus"], to: "Nicol" },
  { from: ["Vreska", "Vraskah", "Raska"], to: "Vraska" },
  { from: ["Raul", "Rall", "Rawl"], to: "Ral" },
  { from: ["Chondra"], to: "Chandra" },
  { from: ["Lilliana", "Lilian", "Lillianna"], to: "Liliana" },
  { from: ["Doven"], to: "Dovin" },
  { from: ["Domry"], to: "Domri" },
  { from: ["Hugin", "Hoogin"], to: "Ugin" },
  { from: ["Tesserik", "Tezzerin", "Tezer", "Tesserit"], to: "Tezzeret" },
  { from: ["Kaeya", "Kaia"], to: "Kaya" },
  { from: ["Pippy"], to: "Pippi" },

  // ── Guilds ──
  { from: ["Boris"], to: "Boros" },
  { from: ["Dimuir", "Dimear"], to: "Dimir" },
  { from: ["Issit", "Izit"], to: "Izzet" },
  { from: ["Orshov", "Orjov"], to: "Orzhov" },
  { from: ["Solicited", "Selenya", "Celenia", "Salinia"], to: "Selesnya" },
  { from: ["Simick", "Simik"], to: "Simic" },
  { from: ["Golgary", "Gulgari"], to: "Golgari" },
  { from: ["Raktos", "Rocktoss"], to: "Rakdos" },
  { from: ["Azorious", "Azorias"], to: "Azorius" },
  { from: ["Grool", "Gruel"], to: "Gruul" },

  // ── Locations ──
  { from: ["Rovnica", "Ravnika"], to: "Ravnica" },
  { from: ["Nividx", "Niviks"], to: "Nivix" },
  { from: ["Scarg", "Skarg"], to: "Skarrg" },
  { from: ["Amonket", "Amoncat"], to: "Amonkhet" },
  { from: ["Ixalon", "Ixlan"], to: "Ixalan" },
  { from: ["Tarker", "Tarkeer"], to: "Tarkir" },
  { from: ["Strixhaven"], to: "Strixhaven" },
  { from: ["Orazka", "Orasca"], to: "Orazca" },

  // ── Artifacts & Items ──
  { from: ["Blazebringr", "Blasebringer"], to: "Blazebringer" },
  { from: ["Scrapy", "Scrappi"], to: "Scrappy" },

  // ── Creatures / Races ──
  { from: ["Teefling"], to: "tiefling" },
  { from: ["Asimar", "Asmar"], to: "aasimar" },
  { from: ["Dragonbourne", "Dragon Born"], to: "dragonborn" },

  // ── D&D Terms ──
  { from: ["Layline"], to: "Leyline" },
  { from: ["Paroon"], to: "Parun" },
  { from: ["Ecuminopolis"], to: "Ecumenopolis" },

  // ── Tarkir ──
  { from: ["Jesskai", "Jeskay"], to: "Jeskai" },
  { from: ["Sultay", "Siltai"], to: "Sultai" },
];


// ══════════════════════════════════════════════════════════════
// HELPER FUNCTIONS
// ══════════════════════════════════════════════════════════════

const readline = require("readline");

function log(msg) {
  const timestamp = new Date().toLocaleTimeString();
  console.log(`[${timestamp}] ${msg}`);
}

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Prompt the user for input on the command line.
 */
function prompt(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => {
    rl.question(question, answer => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

/**
 * List audio files in the recordings directory.
 * Returns an array of { name, fullPath, sizeMB, modified }.
 */
function listRecordings() {
  if (!fs.existsSync(RECORDINGS_DIR)) {
    return [];
  }

  return fs.readdirSync(RECORDINGS_DIR)
    .filter(f => AUDIO_EXTENSIONS.includes(path.extname(f).toLowerCase()))
    .map(f => {
      const fullPath = path.join(RECORDINGS_DIR, f);
      const stats = fs.statSync(fullPath);
      return {
        name: f,
        fullPath,
        sizeMB: (stats.size / (1024 * 1024)).toFixed(1),
        modified: stats.mtime,
      };
    })
    .sort((a, b) => b.modified - a.modified); // newest first
}

/**
 * Upload a local file to AssemblyAI's servers.
 * Returns the upload URL to use for transcription.
 */
async function uploadFile(filePath) {
  log(`Uploading ${path.basename(filePath)}...`);

  const fileData = fs.readFileSync(filePath);
  const response = await fetch(`${BASE_URL}/v2/upload`, {
    method: "POST",
    headers: {
      Authorization: API_KEY,
      "Content-Type": "application/octet-stream",
    },
    body: fileData,
  });

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  log(`Upload complete. URL: ${data.upload_url.substring(0, 60)}...`);
  return data.upload_url;
}

/**
 * Submit a transcription request with Pacts & Power vocabulary config.
 * Returns the transcript ID for polling.
 */
async function submitTranscription(audioUrl) {
  log("Submitting transcription with Pacts & Power vocabulary...");

  const requestBody = {
    audio_url: audioUrl,

    // Use Universal-3 Pro for best accuracy + keyterms support,
    // fall back to Universal-2 if U3 Pro can't handle the audio
    speech_models: ["universal-3-pro", "universal-2"],

    // ── Pacts & Power Campaign Vocabulary ──
    // Boosts recognition of all campaign-specific terms
    keyterms_prompt: PP_KEYTERMS,

    // ── Custom Spelling Corrections ──
    // Post-transcription find-and-replace for common misheard words
    custom_spelling: PP_CUSTOM_SPELLING,

    // ── Speaker Diarization ──
    // Identifies different speakers (DM + 5 players = 6)
    speaker_labels: true,
    speakers_expected: 6,

    // ── General Settings ──
    language_code: "en_us",
    punctuate: true,
    format_text: true,
  };

  const response = await fetch(`${BASE_URL}/v2/transcript`, {
    method: "POST",
    headers: {
      Authorization: API_KEY,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`Submission failed: ${response.status} — ${errorBody}`);
  }

  const data = await response.json();
  log(`Transcription queued. ID: ${data.id}`);
  return data.id;
}

/**
 * Poll until the transcription is complete.
 * Returns the full transcript response object.
 */
async function pollForCompletion(transcriptId) {
  log("Waiting for transcription to complete...");

  const pollUrl = `${BASE_URL}/v2/transcript/${transcriptId}`;
  let dots = 0;

  while (true) {
    const response = await fetch(pollUrl, {
      headers: { Authorization: API_KEY },
    });

    const data = await response.json();

    if (data.status === "completed") {
      log("Transcription complete!");
      return data;
    }

    if (data.status === "error") {
      throw new Error(`Transcription failed: ${data.error}`);
    }

    // Still processing — wait and poll again
    dots = (dots + 1) % 4;
    process.stdout.write(`\r[${new Date().toLocaleTimeString()}] Processing${".".repeat(dots + 1)}${" ".repeat(3 - dots)}`);
    await sleep(5000);
  }
}

/**
 * Format the transcript with speaker labels and timestamps.
 * Outputs in script format compatible with the Pacts & Power workflow.
 */
function formatTranscript(transcriptData) {
  const lines = [];

  lines.push("# Pacts & Power Session Transcript");
  lines.push(`# Transcribed: ${new Date().toISOString()}`);
  lines.push(`# Audio duration: ${Math.round(transcriptData.audio_duration / 60)} minutes`);
  lines.push(`# Model: ${transcriptData.speech_model || "universal-3-pro"}`);
  lines.push(`# Confidence: ${(transcriptData.confidence * 100).toFixed(1)}%`);
  lines.push(`# Speakers expected: 6 (DM + 5 players)`);
  lines.push("");
  lines.push("---");
  lines.push("");

  if (transcriptData.utterances && transcriptData.utterances.length > 0) {
    // Speaker-labeled format
    for (const utterance of transcriptData.utterances) {
      const startTime = formatTimestamp(utterance.start);
      const speaker = utterance.speaker || "UNKNOWN";
      const confidence = (utterance.confidence * 100).toFixed(0);

      lines.push(`[${startTime}] SPEAKER ${speaker}: ${utterance.text}`);
      lines.push("");
    }
  } else {
    // Plain text fallback (no speaker labels)
    lines.push(transcriptData.text);
  }

  return lines.join("\n");
}

/**
 * Convert milliseconds to HH:MM:SS timestamp format.
 */
function formatTimestamp(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
}


// ══════════════════════════════════════════════════════════════
// MAIN
// ══════════════════════════════════════════════════════════════

async function main() {
  const args = process.argv.slice(2);

  // Validate API key early
  if (API_KEY === "YOUR_API_KEY_HERE") {
    console.error("ERROR: Set your AssemblyAI API key first.");
    console.error("  set ASSEMBLYAI_API_KEY=your_key_here");
    console.error("  — or add it to .env in the Workflows folder.");
    process.exit(1);
  }

  let input;
  let outputPath;

  if (args.length === 0) {
    // ── Interactive mode: list recordings and let user pick ──
    console.log(`
╔══════════════════════════════════════════════════╗
║   Pacts & Power AssemblyAI Transcriber           ║
║   The Breakfast Club Campaign                    ║
╚══════════════════════════════════════════════════╝
`);
    console.log(`Recordings folder: ${RECORDINGS_DIR}`);
    console.log(`Vocabulary loaded:  ${PP_KEYTERMS.length} keyterms`);
    console.log(`Custom spellings:   ${PP_CUSTOM_SPELLING.length} correction rules\n`);

    const recordings = listRecordings();

    if (recordings.length === 0) {
      console.log("No audio files found in the recordings folder.");
      console.log(`Looked in: ${RECORDINGS_DIR}`);
      console.log(`\nYou can also pass a file path directly:`);
      console.log(`  node pp_transcribe.js "C:\\path\\to\\recording.mp3"\n`);
      process.exit(0);
    }

    console.log("Available recordings (newest first):\n");
    recordings.forEach((r, i) => {
      const date = r.modified.toLocaleDateString("en-US", {
        month: "2-digit", day: "2-digit", year: "2-digit"
      });
      console.log(`  [${i + 1}]  ${r.name}  (${r.sizeMB} MB, ${date})`);
    });

    console.log(`\n  [0]  Enter a custom file path`);
    console.log("");

    const choice = await prompt("Pick a file number: ");
    const choiceNum = parseInt(choice, 10);

    if (choiceNum === 0) {
      input = await prompt("Enter file path or URL: ");
    } else if (choiceNum >= 1 && choiceNum <= recordings.length) {
      input = recordings[choiceNum - 1].fullPath;
    } else {
      console.error("Invalid selection.");
      process.exit(1);
    }

    console.log("");
  } else {
    // ── CLI mode: file path passed as argument ──
    input = args[0];
    outputPath = args[1] || null;
  }

  let audioUrl;

  // Determine if input is a URL or local file
  if (input.startsWith("http://") || input.startsWith("https://")) {
    audioUrl = input;
    log(`Using remote URL: ${input}`);
  } else {
    // If just a filename (no path separators), look in RECORDINGS_DIR
    if (!input.includes(path.sep) && !input.includes("/")) {
      const inRecordings = path.join(RECORDINGS_DIR, input);
      if (fs.existsSync(inRecordings)) {
        input = inRecordings;
      }
    }

    if (!fs.existsSync(input)) {
      console.error(`ERROR: File not found: ${input}`);
      console.error(`Also checked: ${path.join(RECORDINGS_DIR, path.basename(input))}`);
      process.exit(1);
    }
    audioUrl = await uploadFile(input);
  }

  // Submit and poll
  const transcriptId = await submitTranscription(audioUrl);
  const result = await pollForCompletion(transcriptId);

  // Format output
  const formatted = formatTranscript(result);

  // Determine output path — default to Transcripts/Raw_Unedited
  if (!outputPath) {
    // Create Transcripts subfolder if it doesn't exist
    if (!fs.existsSync(TRANSCRIPTS_DIR)) {
      fs.mkdirSync(TRANSCRIPTS_DIR, { recursive: true });
      log(`Created output folder: ${TRANSCRIPTS_DIR}`);
    }
    const baseName = path.basename(input).replace(/\.[^.]+$/, "");
    outputPath = path.join(TRANSCRIPTS_DIR, `${baseName}_transcript.md`);
  }

  fs.writeFileSync(outputPath, formatted, "utf-8");
  log(`Transcript saved to: ${outputPath}`);

  // Print summary
  console.log(`
╔══════════════════════════════════════════════════╗
║   Transcription Complete                         ║
╠══════════════════════════════════════════════════╣
║  Duration:    ${String(Math.round(result.audio_duration / 60) + " minutes").padEnd(34)}║
║  Confidence:  ${String((result.confidence * 100).toFixed(1) + "%").padEnd(34)}║
║  Words:       ${String(result.words?.length || "N/A").padEnd(34)}║
║  Speakers:    ${String(result.utterances?.length ? new Set(result.utterances.map(u => u.speaker)).size : "N/A").padEnd(34)}║
║  Output:      ${String(path.basename(outputPath)).padEnd(34)}║
║  Saved to:    ${String(path.dirname(outputPath)).substring(0, 34).padEnd(34)}║
╚══════════════════════════════════════════════════╝
`);
}

main().catch(err => {
  console.error(`\nERROR: ${err.message}`);
  process.exit(1);
});
