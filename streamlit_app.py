import streamlit as st
from ai_recommender import CareerRecommender

st.set_page_config(page_title="Career Recommender AI", layout="centered")

st.title("🎯 AI Career Path Recommender")

# Load recommender
rec = CareerRecommender("tech_roles.csv")


st.subheader("📊 Available Skills in Database")


all_skills = sorted(rec.vocab) if hasattr(rec, 'vocab') else []
st.info(f"📌 **{len(all_skills)} skills available** in the database")



def categorize_skill(skill):
 
    skill_lower = skill.lower()
    
    categories = {
        "🐍 Programming Languages": ["python", "java", "javascript", "c++", "c#", "kotlin", "swift", "go", "ruby", "php", "typescript", "c", "r"],
        "🤖 Machine Learning & AI": ["machine learning", "deep learning", "tensorflow", "pytorch", "keras", "scikit", "nlp", "llm", "transformers", "openai", "langchain", "mlops", "ai", "computer vision", "opencv"],
        "📊 Data Science & Analytics": ["statistics", "math", "pandas", "numpy", "data visualization", "tableau", "power bi", "excel", "business intelligence", "data analysis"],
        "🗄️ Databases": ["sql", "database", "postgresql", "mysql", "mongodb", "redis", "cassandra", "big data", "spark", "hadoop", "etl", "airflow"],
        "☁️ Cloud & DevOps": ["cloud computing", "aws", "azure", "gcp", "docker", "kubernetes", "linux", "ci/cd", "jenkins", "gitlab", "automation", "terraform", "ansible"],
        "🌐 Web Development": ["html", "css", "javascript", "react", "angular", "vue", "node.js", "django", "flask", "fastapi", "api", "rest"],
        "📱 Mobile Development": ["flutter", "react native", "swift", "kotlin", "android", "ios", "firebase", "xamarin"],
        "🔒 Cybersecurity": ["security", "network security", "ethical hacking", "penetration testing", "risk analysis", "compliance", "cybersecurity", "cryptography"],
        "🛠️ Software Engineering": ["oop", "dsa", "system design", "git", "github", "testing", "debugging", "agile", "scrum", "game physics", "unity", "unreal"],
        "📡 Networking & IT": ["networking", "hardware", "windows", "linux admin", "server", "troubleshooting", "it support", "system administration"]
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in skill_lower:
                return category
    
    return "📁 Other Skills"




categorized_skills = {}
for skill in all_skills:
    cat = categorize_skill(skill)
    if cat not in categorized_skills:
        categorized_skills[cat] = []
    categorized_skills[cat].append(skill)


category_order = [
    "🐍 Programming Languages",
    "🤖 Machine Learning & AI",
    "📊 Data Science & Analytics",
    "🗄️ Databases",
    "☁️ Cloud & DevOps",
    "🌐 Web Development",
    "📱 Mobile Development",
    "🔒 Cybersecurity",
    "🛠️ Software Engineering",
    "📡 Networking & IT",
    "📁 Other Skills"
]



st.subheader("📝 Select Your Technical Skills")

selected_skills = []

# Create tabs for better organization
tabs = st.tabs([cat.split()[1] if len(cat.split()) > 1 else cat[:10] for cat in category_order if cat in categorized_skills])

for tab, category in zip(tabs, [cat for cat in category_order if cat in categorized_skills]):
    with tab:
        skills_in_cat = sorted(categorized_skills[category])
        st.markdown(f"**{category}** ({len(skills_in_cat)} skills)")
        
        
        cols = st.columns(4)
        for idx, skill in enumerate(skills_in_cat):
            col_idx = idx % 4
            with cols[col_idx]:
                if st.checkbox(skill, key=f"skill_{skill}"):
                    selected_skills.append(skill)

st.divider()
if selected_skills:
    st.success(f"✅ **Selected Skills ({len(selected_skills)})**: {', '.join(selected_skills)}")
else:
    st.info("📌 Click on the checkboxes above to select your skills")

st.divider()



if st.button("🎯 Recommend Me a Career", type="primary", use_container_width=True):
    if len(selected_skills) < 1:
        st.warning("⚠️ Please select at least one skill")
    else:
        with st.spinner("🤖 Analyzing your skills..."):
            results = rec.recommend(selected_skills)
        
        st.success(f"✨ Found {len(results)} career matches!")
        
        for i, r in enumerate(results, 1):
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{i}. {r['role']}")
                with col2:
                    percent = int(r['score'] * 100)
                    st.markdown(f"### 🟢 {percent}%" if percent >= 70 else f"### 🟡 {percent}%")
                
                # Job details
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("**📂 Category**")
                    st.write(r.get('category', 'N/A'))
                with c2:
                    st.markdown("**📊 Level**")
                    st.write(r.get('level', 'N/A'))
                with c3:
                    st.markdown("**💰 Salary**")
                    st.write(r.get('salary', 'N/A'))
                
                st.markdown("---")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("### ✅ Your Matched Skills")
                    matched = r.get('matched', [])
                    if matched:
                        for skill in matched:
                            st.markdown(f"- `{skill}`")
                    else:
                        st.caption("No direct matches")
                
                with col_b:
                    st.markdown("### 📚 Missing Skills")
                    missing = r.get('missing', [])
                    if missing:
                        for skill in missing[:5]:
                            st.markdown(f"- `{skill}`")
                    else:
                        st.caption("You have all skills! 🎉")
                
                st.markdown("---")

# ========== SIDEBAR ==========

with st.sidebar:
    st.markdown("## 📊 Database Stats")
    st.metric("Total Job Roles", len(rec.roles) if hasattr(rec, 'roles') else "N/A")
    st.metric("Total Skills", len(all_skills))
    
    st.divider()
    
    st.markdown("## 📁 Categories")
    for cat, skills in categorized_skills.items():
        st.caption(f"- {cat}: {len(skills)} skills")