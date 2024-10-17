import random

class BioGenerator:
    def __init__(self):
        self.adjectives = [
            "Crypto", "Blockchain", "DeFi", "NFT", "Web3", "Tech", "Digital",
            "Innovative", "Forward-thinking", "Passionate", "Experienced",
            "Strategic", "Creative", "Tech-savvy", "Visionary", "Curious",
            "Analytical", "Goal-oriented", "Progressive", "Enthusiastic",
            "Disruptive", "Agile", "Futuristic", "Cutting-edge", "Pioneering",
            "Ambitious", "Dynamic", "Resourceful", "Adaptable", "Insightful"
        ]

        self.nouns = [
            "Enthusiast", "Explorer", "Innovator", "Visionary", "Pioneer",
            "Developer", "Investor", "Entrepreneur", "Marketer", "Strategist",
            "Analyst", "Consultant", "Advisor", "Researcher", "Technologist",
            "Founder", "Engineer", "Designer", "Influencer", "Thinker",
            "Architect", "Evangelist", "Catalyst", "Futurist", "Mentor",
            "Trailblazer", "Advocate", "Leader", "Specialist", "Maverick"
        ]

        self.interests = [
            "AI", "Blockchain", "Cryptocurrency", "Startups", "FinTech",
            "DeFi", "NFTs", "Web3", "Metaverse", "Tokenization", "Smart Contracts",
            "Decentralization", "SaaS", "Cloud Computing", "DApps",
            "Digital Art", "Trading", "Programming", "Sustainability",
            "Machine Learning", "IoT", "Quantum Computing", "AR/VR", "Cybersecurity",
            "Big Data", "Robotics", "Space Tech", "Biotech", "Green Energy",
            "5G", "Edge Computing", "Digital Identity", "Predictive Analytics"
        ]

        self.actions = [
            "Exploring", "Building", "Learning", "Teaching", "Developing",
            "Investing in", "Creating", "Shaping", "Innovating", "Scaling",
            "Consulting on", "Researching", "Connecting", "Growing", "Helping",
            "Disrupting", "Empowering", "Transforming", "Advising on",
            "Pioneering", "Revolutionizing", "Accelerating", "Optimizing",
            "Envisioning", "Architecting", "Evangelizing", "Implementing",
            "Strategizing", "Mentoring", "Collaborating on"
        ]

        self.closing_statements = [
            "Always curious.", "Embracing the future.", "Pushing the limits.",
            "Here for the ride.", "Ready to change the world.",
            "Bringing ideas to life.", "Open to new ideas.",
            "Driven by innovation.", "Lifelong learner.", "Let's connect!",
            "Turning challenges into opportunities.", "Dream. Believe. Achieve.",
            "Coding the future.", "Breaking barriers.", "Bridging the gap.",
            "Innovate or evaporate.", "Think big, start small, scale fast.",
            "Creating ripples of change.", "Passionate about possibilities.",
            "Where technology meets creativity."
        ]

        self.emojis = ["🚀", "🌐", "💡", "🔗", "📈", "💻", "📊", "🌱", "⚡️", "💎", "🔥", "🔮",
                       "🎯", "🧠", "🌈", "🏆", "🔬", "🛠️", "🔐", "🌟", "🔄", "🧩", "🎨", "🔋"]

        self.quotes = [
            "The future belongs to those who believe in the beauty of their dreams.",
            "Innovation distinguishes between a leader and a follower.",
            "The only way to do great work is to love what you do.",
            "Dream big, start small, but most of all, start.",
            "The best way to predict the future is to create it.",
            "Stay hungry, stay foolish.",
            "Think differently.",
            "Move fast and break things.",
            "Done is better than perfect.",
            "Make it work, make it right, make it fast."
        ]

    def generate_bio(self):
        bio_type = random.choice([
            "standard", "action_oriented", "philosophical", "minimalist",
            "emoji_heavy", "techy", "question_based", "goal_oriented",
            "creative", "professional"
        ])

        bio = getattr(self, f"_generate_{bio_type}_bio")()

        if len(bio) > 70:
            bio = bio[:67] + "..."

        return bio

    def _generate_standard_bio(self):
        adjective = random.choice(self.adjectives)
        noun = random.choice(self.nouns)
        interest = random.choice(self.interests)
        emoji = random.choice(self.emojis)

        return f"{adjective} {noun}. {interest} {emoji}"

    def _generate_action_oriented_bio(self):
        action = random.choice(self.actions)
        interest = random.choice(self.interests)
        emoji = random.choice(self.emojis)

        return f"{action} {interest} {emoji}"

    def _generate_philosophical_bio(self):
        quote = random.choice(self.quotes)
        return quote[:70]

    def _generate_minimalist_bio(self):
        noun = random.choice(self.nouns)
        interest = random.choice(self.interests)
        emoji = random.choice(self.emojis)

        return f"{noun}. {interest}. {emoji}"

    def _generate_emoji_heavy_bio(self):
        adjective = random.choice(self.adjectives)
        noun = random.choice(self.nouns)
        emojis = ''.join(random.sample(self.emojis, 3))

        return f"{emojis} {adjective} {noun}"

    def _generate_techy_bio(self):
        interests = random.sample(self.interests, 2)
        emoji = random.choice(self.emojis)

        return f"< {interests[0]} /> {{ {interests[1]} }} {emoji}"

    def _generate_question_based_bio(self):
        interest = random.choice(self.interests)
        emoji = random.choice(self.emojis)

        return f"Revolutionizing {interest}? {emoji}"

    def _generate_goal_oriented_bio(self):
        action = random.choice(self.actions)
        interest = random.choice(self.interests)
        emoji = random.choice(self.emojis)

        return f"Mission: {action} {interest} {emoji}"

    def _generate_creative_bio(self):
        adjectives = random.sample(self.adjectives, 2)
        interest = random.choice(self.interests)
        emoji = random.choice(self.emojis)

        return f"{adjectives[0]}. {adjectives[1]}. {interest}. {emoji}"

    def _generate_professional_bio(self):
        noun = random.choice(self.nouns)
        interest = random.choice(self.interests)

        return f"{noun} specializing in {interest}"