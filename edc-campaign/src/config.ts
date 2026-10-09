/**
 * EDIT HERE. Every word and every colour in the film lives in this file.
 * Timing (scene starts, beat grid) lives in ../timeline.json so the
 * soundtrack generator can read the same numbers.
 */

export const COLORS = {
  ink: "#111111", // main dark background, text on light scenes
  paper: "#F2EDE3", // main light background, text on dark scenes
  accent: "#FF4A1C", // vermilion: the box, highlights, key numbers
  stone: "#8E887C", // secondary text, inactive elements
  graphite: "#262626", // panels and inactive grid cells on dark scenes
} as const;

export const FONTS = {
  display: "Archivo", // variable: wdth 62–125, wght 100–900
  mono: "JetBrains Mono", // variable: wght 100–800
} as const;

export const TEXT = {
  hook: {
    kicker: "EDC · NIAT–S-VYASA UNIVERSITY",
    line1: ["Everyone", "has", "a", "startup", "idea."],
    line2Before: "Who’s actually",
    line2Highlight: "building",
    line2After: "one?",
  },

  name: {
    first: "KARAN",
    last: "RAJ KR",
    tag: "Founder, KĀRYO", // always KĀRYO with the macron
    detail: "B.Tech CSE (AI/ML) · NIAT–S-VYASA University, Bengaluru",
  },

  builds: {
    kicker: "01 — Builds",
    headline: ["Real products.", "Real revenue."],
    stats: [
      { value: "6-figure revenue", label: "Products & agencies" },
      { value: "18 merged PRs", label: "GSSoC 2026" },
    ],
    products: [
      {
        tab: "School ERP",
        url: "erpdemo.karanrajkr.com",
        title: "School ERP",
        line: "Live at erpdemo.karanrajkr.com",
        chips: ["41 tables", "~45 routes", "Live"],
      },
      {
        tab: "ClinicDesk",
        url: "clinicdesk",
        title: "ClinicDesk",
        line: "Dental clinic system.",
        chips: [],
      },
      {
        tab: "Eligent",
        url: "eligent",
        title: "Eligent",
        line: "Finds it. Checks eligibility. Fills the form.",
        chips: [],
      },
      {
        tab: "FormPilot",
        url: "formpilot · chrome extension",
        title: "FormPilot",
        line: "AI Chrome extension.",
        chips: [],
      },
    ],
  },

  wins: {
    kicker: "02 — Wins",
    event: "OPEN LOOP 2026",
    eventPlace: "Yenepoya, Mangaluru",
    teams: "121 teams",
    legend: "1 square = 1 team",
    facts: "309 participants · 109 colleges · 14 states",
    result: "1ST PLACE",
    product: "with FormPilot",
    scoreUs: { label: "Our score", value: 80 },
    scoreThem: { label: "Runner-up", value: 60 },
    prize: "₹20,000 prize",
    awards: [
      { name: "GRIT Awards 2026", detail: "Winner · Content + Hackathons" },
      { name: "HackBLR 2026", detail: "Top 40 of 2,500+ teams" },
      { name: "Technology Innovators Award", detail: "August 2026" },
      { name: "IIT Alumni Incubation", detail: "Selected · Cohort 2.0" },
    ],
  },

  people: {
    kicker: "03 — People",
    headline: "Co-led 4+ events",
    events: [
      "IPL Auction",
      "30-Min Build\n+ Pitch",
      "Every Team\nSponsored",
      "Debate &\nRebrand",
    ],
    crowdCount: 120,
    crowdSuffix: "+",
    crowdLine1: "at our biggest event",
    crowdLine2: "— and teams kept building after.",
  },

  pledges: {
    kicker: "My 3 promises for EDC",
    items: [
      {
        title: "HACKATHONS",
        line: "A campus hackathon this year. Then a national one.",
      },
      {
        title: "INTERNSHIPS",
        line: "For students, through my company.",
      },
      {
        title: "BUILD & PITCH NIGHTS",
        line: "Every month. Ideas into products.",
      },
    ],
  },

  vote: {
    verb: "VOTE",
    name: "KARAN RAJ KR",
    role: "for EDC President",
    date: "", // e.g. "Voting: 24 Oct" — leave empty to hide
    links: "karanrajkr.com · @karan.rajkr",
  },
} as const;
