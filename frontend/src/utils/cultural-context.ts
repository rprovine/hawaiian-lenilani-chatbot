export const hawaiianValues = {
  aloha: {
    name: 'Aloha',
    meaning: 'Love, affection, peace, compassion, mercy',
    businessApplication: 'Build genuine relationships with care and respect',
    emoji: '🌺',
  },
  ohana: {
    name: 'Ohana',
    meaning: 'Family, including extended family and close friends',
    businessApplication: 'Treat business partners and customers as family',
    emoji: '👨‍👩‍👧‍👦',
  },
  malama_aina: {
    name: 'Malama ʻĀina',
    meaning: 'To care for and honor the land',
    businessApplication: 'Practice environmental responsibility and sustainability',
    emoji: '🌿',
  },
  lokahi: {
    name: 'Lokahi',
    meaning: 'Unity, agreement, harmony',
    businessApplication: 'Work together in harmony for mutual success',
    emoji: '🤝',
  },
  kuleana: {
    name: 'Kuleana',
    meaning: 'Responsibility, jurisdiction, privilege',
    businessApplication: 'Take responsibility for community impact',
    emoji: '💫',
  },
  pono: {
    name: 'Pono',
    meaning: 'Righteousness, balance, correctness',
    businessApplication: 'Conduct business with integrity and balance',
    emoji: '⚖️',
  },
};

export const pidginExpressions = {
  greetings: {
    'howzit': 'How are you?',
    'aloha': 'Hello/Goodbye/Love',
    'shoots': 'Okay/Sounds good',
    'rajah': 'Okay/Understood',
  },
  business: {
    'talk story': 'Have a conversation',
    'pau hana': 'After work',
    'da kine': 'The thing/stuff',
    'broke da mouth': 'Delicious',
    'choke': 'A lot/Many',
    'grindz': 'Food',
  },
  affirmations: {
    'can': 'Yes/Able to',
    'no can': 'No/Unable to',
    'yeah no': 'No',
    'no yeah': 'Yes',
    'k den': 'Okay then',
  },
  expressions: {
    'brah/bruddah': 'Brother/Friend',
    'sistah': 'Sister/Friend',
    'stay': 'Is/Are (ongoing state)',
    'ono': 'Delicious',
    'lolo': 'Crazy',
    'da buggah': 'That thing',
  },
};

export const islandCharacteristics = {
  oahu: {
    nickname: 'The Gathering Place',
    emoji: '🏙️',
    characteristics: [
      'Urban and diverse',
      'Business hub of Hawaii',
      'Mix of local and international',
      'Fast-paced island life',
    ],
    businessStyle: 'Professional with aloha',
  },
  maui: {
    nickname: 'The Valley Isle',
    emoji: '🌺',
    characteristics: [
      'Luxury and leisure',
      'Strong tourism focus',
      'Laid-back atmosphere',
      'Environmental consciousness',
    ],
    businessStyle: 'Relaxed professionalism',
  },
  big_island: {
    nickname: 'The Orchid Isle',
    emoji: '🌋',
    characteristics: [
      'Diverse landscapes',
      'Agricultural heritage',
      'Entrepreneurial spirit',
      'Close-knit communities',
    ],
    businessStyle: 'Independent and innovative',
  },
  kauai: {
    nickname: 'The Garden Isle',
    emoji: '🌿',
    characteristics: [
      'Natural beauty focused',
      'Small-town feel',
      'Environmental priority',
      'Tight community bonds',
    ],
    businessStyle: 'Community-oriented',
  },
};

export const culturalProtocols = {
  meetings: {
    start: 'Begin with personal connection and aloha',
    during: 'Allow time for relationship building',
    end: 'Close with gratitude and next steps',
    time: 'Be flexible with "island time" but respectful',
  },
  communication: {
    style: 'Indirect and harmonious',
    feedback: 'Gentle and constructive',
    disagreement: 'Respectful and solution-focused',
    humor: 'Appreciated but respectful',
  },
  relationships: {
    building: 'Take time to know the person first',
    maintaining: 'Regular check-ins beyond business',
    trust: 'Earned through consistent actions',
    reciprocity: 'Give without expecting immediate return',
  },
};

export const businessEtiquette = {
  greetings: [
    'Offer a warm smile and aloha',
    'Handshake or hug depending on relationship',
    'Ask about family and well-being',
    'Share a bit about yourself',
  ],
  gifts: [
    'Small gifts are appreciated',
    'Local products are preferred',
    'Present with both hands',
    'Accept graciously',
  ],
  dining: [
    'Share food generously',
    'Try everything offered',
    'Compliment the food',
    'Offer to help clean up',
  ],
  respect: [
    'Respect kupuna (elders)',
    'Honor local customs',
    'Learn basic Hawaiian words',
    'Support local businesses',
  ],
};

export const getCulturalContext = (
  businessType?: string,
  island?: string
): { values: string[]; tips: string[] } => {
  const values = [];
  const tips = [];

  // Add relevant values based on business type
  if (businessType === 'tourism') {
    values.push('aloha', 'lokahi');
    tips.push('Focus on authentic experiences', 'Respect sacred places');
  } else if (businessType === 'agriculture') {
    values.push('malama_aina', 'kuleana');
    tips.push('Emphasize sustainability', 'Connect with land heritage');
  } else if (businessType === 'restaurant') {
    values.push('ohana', 'aloha');
    tips.push('Create family atmosphere', 'Source locally when possible');
  }

  // Add island-specific tips
  if (island && island in islandCharacteristics) {
    const islandInfo = islandCharacteristics[island as keyof typeof islandCharacteristics];
    tips.push(`Embrace ${islandInfo.businessStyle}`);
  }

  return { values, tips };
};