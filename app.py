"""
AI Healthcare Coaching Platform - Streamlit Demo
Installation: pip install streamlit pandas plotly
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import random

# Page configuration
st.set_page_config(
    page_title="AI Coaching Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .persona-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .chat-message-user {
        background-color: #3b82f6;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        margin-left: 20%;
    }
    .chat-message-ai {
        background-color: #f3f4f6;
        color: #1f2937;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        margin-right: 20%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = None
if 'conversation_active' not in st.session_state:
    st.session_state.conversation_active = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_complete' not in st.session_state:
    st.session_state.session_complete = False
if 'ai_assessment' not in st.session_state:
    st.session_state.ai_assessment = None

# HCP Personas Data
personas = {
    "Dr. Sarah Chen": {
        "specialty": "Cardiologist",
        "experience": "15 years",
        "personality": "Data-driven, skeptical of new treatments",
        "context": "Busy practice, values efficiency",
        "difficulty": "Hard",
        "objections": ["Need more clinical data", "Current treatment works fine", "Cost concerns"],
        "avatar": "👩‍⚕️"
    },
    "Dr. Michael Roberts": {
        "specialty": "General Practitioner",
        "experience": "8 years",
        "personality": "Open to innovation, patient-focused",
        "context": "Growing practice, interested in new solutions",
        "difficulty": "Medium",
        "objections": ["Patient acceptance", "Insurance coverage", "Training requirements"],
        "avatar": "👨‍⚕️"
    },
    "Dr. Emily Watson": {
        "specialty": "Oncologist",
        "experience": "20 years",
        "personality": "Conservative, evidence-based",
        "context": "Academic hospital setting",
        "difficulty": "Hard",
        "objections": ["Peer-reviewed studies needed", "Hospital formulary process", "Side effect profile"],
        "avatar": "👩‍⚕️"
    }
}

# AI Response Generator
def generate_ai_response(persona_name, user_message):
    """Simulate AI responses based on persona"""
    responses = [
        "I appreciate the information, but I'd need to see more robust clinical trial data before considering this for my patients. What Phase III results do you have?",
        "That's interesting. How does this compare to the current standard of care in terms of efficacy and safety profile?",
        "I'm concerned about the cost. Many of my patients struggle with medication affordability. What patient assistance programs are available?",
        "Can you walk me through the mechanism of action? I want to understand how this differs from existing treatments.",
        "What's the evidence on long-term outcomes? I'm particularly interested in real-world data beyond the clinical trials.",
        "I've had good results with the current treatment protocol. What would be the compelling reason for me to switch?",
        "How does this fit into the current treatment guidelines? Has it been incorporated into any professional society recommendations?",
        "What kind of monitoring is required? I need to understand the practical implications for my practice."
    ]
    return random.choice(responses)

# AI Assessment Generator - Generic Assessment
def generate_ai_assessment(messages, persona):
    """Generate a generic comprehensive AI assessment"""
    
    # Fixed assessment scores for demo
    base_scores = {
        'Clinical Knowledge': 87,
        'Rapport Building': 92,
        'Objection Handling': 78,
        'Value Communication': 85,
        'Compliance & Ethics': 95
    }
    
    overall_score = 87
    weak_areas = ['Objection Handling']
    strong_areas = ['Rapport Building', 'Compliance & Ethics']
    
    # Generic insights
    insights = [
        "🎯 **Objection Handling:** Practice preemptively addressing common objections before they're raised. Use the LAER model (Listen, Acknowledge, Explore, Respond).",
        "💪 **Strong Rapport Building:** Excellent ability to establish trust and credibility quickly with healthcare professionals.",
        "✅ **Compliance Excellence:** Outstanding adherence to regulatory and ethical guidelines throughout the conversation."
    ]
    
    # LMS recommendations for weak areas
    lms_recommendations = [
        {
            'title': 'LAER Objection Handling Framework',
            'type': 'Interactive Module',
            'duration': '60 min',
            'priority': 'High',
            'link': 'https://lms.example.com/laer-framework',
            'description': 'Master the Listen-Acknowledge-Explore-Respond methodology with practice scenarios'
        },
        {
            'title': 'Top 20 HCP Objections & Responses',
            'type': 'Reference Guide',
            'duration': '15 min',
            'priority': 'High',
            'link': 'https://lms.example.com/objection-library',
            'description': 'Comprehensive library of proven responses to common objections'
        },
        {
            'title': 'Advanced Objection Handling Role-Plays',
            'type': 'Video Series',
            'duration': '45 min',
            'priority': 'Medium',
            'link': 'https://lms.example.com/objection-videos',
            'description': 'Watch expert sales reps handle difficult objections in real-world scenarios'
        }
    ]
    
    # Scenario recommendations
    scenario_recommendations = [
        {
            'title': 'Deep Objection Handling Practice',
            'difficulty': 'Intermediate-Advanced',
            'description': 'Face 5+ consecutive objections from a highly skeptical HCP',
            'personas': ['Dr. Sarah Chen', 'Dr. Emily Watson'],
            'estimated_time': '15-20 min',
            'skills_developed': ['Persistence', 'Objection reframing', 'Emotional resilience']
        },
        {
            'title': 'Multi-Stakeholder Account Meeting',
            'difficulty': 'Advanced',
            'description': 'Navigate complex group dynamics with department heads, formulary committee members, and budget holders',
            'personas': ['Chief of Cardiology', 'Pharmacy Director', 'CFO'],
            'estimated_time': '25-30 min',
            'skills_developed': ['Stakeholder management', 'Budget negotiation', 'Group influence']
        }
    ]
    
    return {
        'overall_score': overall_score,
        'category_scores': base_scores,
        'weak_areas': weak_areas,
        'strong_areas': strong_areas,
        'insights': insights,
        'lms_recommendations': lms_recommendations,
        'scenario_recommendations': scenario_recommendations,
        'skill_level_update': 'intermediate'
    }

# Sidebar Navigation
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/3b82f6/ffffff?text=AI+Coach", use_container_width=True)
    st.markdown("### Navigation")
    
    if st.button("🏠 Dashboard", use_container_width=True, type="primary" if st.session_state.page == 'dashboard' else "secondary"):
        st.session_state.page = 'dashboard'
        st.session_state.conversation_active = False
        st.session_state.session_complete = False
        st.rerun()
    
    if st.button("🎭 Practice Sessions", use_container_width=True, type="primary" if st.session_state.page == 'personas' else "secondary"):
        st.session_state.page = 'personas'
        st.session_state.conversation_active = False
        st.session_state.session_complete = False
        st.rerun()
    
    if st.button("📊 Analytics", use_container_width=True, type="primary" if st.session_state.page == 'analytics' else "secondary"):
        st.session_state.page = 'analytics'
        st.session_state.conversation_active = False
        st.session_state.session_complete = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    st.metric("Sessions Completed", "24", "+3")
    st.metric("Average Score", "86%", "+5%")
    st.metric("Practice Time", "12h", "+2h")

# DASHBOARD PAGE
if st.session_state.page == 'dashboard':
    st.markdown('<div class="main-header">🎯 AI Coaching Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Practice and improve your healthcare professional interactions</div>', unsafe_allow_html=True)
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📈 Sessions Completed",
            value="24",
            delta="3 this week"
        )
    
    with col2:
        st.metric(
            label="⭐ Average Score",
            value="86%",
            delta="5%"
        )
    
    with col3:
        st.metric(
            label="⏱️ Practice Time",
            value="12h",
            delta="2h this week"
        )
    
    with col4:
        st.metric(
            label="🏆 Achievements",
            value="8",
            delta="2 new"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Actions and Recent Activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Quick Start")
        if st.button("▶️ Start New Roleplay Session", use_container_width=True, type="primary"):
            st.session_state.page = 'personas'
            st.rerun()
        
        if st.button("📊 View Performance Analytics", use_container_width=True):
            st.session_state.page = 'analytics'
            st.rerun()
    
    with col2:
        st.markdown("### 📋 Recent Activity")
        st.markdown("""
        <div class="success-box">
            <strong>✅ Session with Dr. Chen completed</strong><br>
            Score: 88% - 2 hours ago
        </div>
        <div style="background-color: #dbeafe; border-left: 4px solid #3b82f6; padding: 1rem; border-radius: 0.25rem;">
            <strong>💬 New feedback available</strong><br>
            Manager review - 1 day ago
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Learning Path Recommendations
    st.markdown("### 🎓 Learning Path Recommendations")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="persona-card">
            <h4>🎯 Objection Handling</h4>
            <p>Improve your response to clinical objections</p>
            <span style="background-color: #fef3c7; color: #92400e; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.75rem;">Priority: High</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="persona-card">
            <h4>💰 Value Communication</h4>
            <p>Strengthen economic value discussions</p>
            <span style="background-color: #dbeafe; color: #1e40af; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.75rem;">Priority: Medium</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="persona-card">
            <h4>🏆 Advanced Scenarios</h4>
            <p>Ready for complex multi-stakeholder calls</p>
            <span style="background-color: #d1fae5; color: #065f46; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.75rem;">Priority: Low</span>
        </div>
        """, unsafe_allow_html=True)

# PERSONAS/PRACTICE PAGE
elif st.session_state.page == 'personas':
    if not st.session_state.conversation_active and not st.session_state.session_complete:
        st.markdown('<div class="main-header">🎭 Select Healthcare Professional</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Choose a persona to practice your interaction skills</div>', unsafe_allow_html=True)
        
        # Difficulty Filter
        difficulty = st.selectbox("🎚️ Difficulty Level", ["All Levels", "Easy", "Medium", "Hard"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display Personas
        for name, details in personas.items():
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="persona-card">
                        <h3>{details['avatar']} {name}</h3>
                        <p style="color: #3b82f6; font-weight: bold;">{details['specialty']}</p>
                        <p><strong>Experience:</strong> {details['experience']}</p>
                        <p><strong>Personality:</strong> {details['personality']}</p>
                        <p><strong>Context:</strong> {details['context']}</p>
                        <p><strong>Common Objections:</strong> {', '.join(details['objections'])}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<br><br>", unsafe_allow_html=True)
                    difficulty_color = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}
                    st.markdown(f"### {difficulty_color.get(details['difficulty'], '🟡')} {details['difficulty']}")
                    if st.button(f"▶️ Start Session", key=f"start_{name}", use_container_width=True, type="primary"):
                        st.session_state.selected_persona = name
                        st.session_state.conversation_active = True
                        st.session_state.messages = [
                            {"role": "ai", "content": f"Good morning, I'm {name}. I understand you wanted to speak with me about a new treatment option? I have about 10 minutes before my next patient.", "time": datetime.now()}
                        ]
                        st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    # CONVERSATION SCREEN
    elif st.session_state.conversation_active:
        persona_name = st.session_state.selected_persona
        persona = personas[persona_name]
        
        # Header
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"### {persona['avatar']} {persona_name}")
            st.caption(f"{persona['specialty']} • {persona['difficulty']} Difficulty")
        
        with col2:
            if st.button("🔄 Switch Persona", use_container_width=True):
                st.session_state.conversation_active = False
                st.session_state.messages = []
                st.rerun()
        
        with col3:
            if st.button("✅ End Session", use_container_width=True, type="primary"):
                # Generate AI assessment
                with st.spinner("🤖 AI is analyzing your performance..."):
                    time.sleep(2)
                    st.session_state.ai_assessment = generate_ai_assessment(
                        st.session_state.messages, 
                        personas[st.session_state.selected_persona]
                    )
                st.session_state.conversation_active = False
                st.session_state.session_complete = True
                st.rerun()
        
        st.markdown("---")
        
        # Chat Container
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message-user">
                        <strong>You:</strong><br>
                        {message['content']}
                        <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;">
                            {message['time'].strftime('%H:%M:%S')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message-ai">
                        <strong>{persona['avatar']} {persona_name}:</strong><br>
                        {message['content']}
                        <div style="font-size: 0.75rem; opacity: 0.6; margin-top: 0.5rem;">
                            {message['time'].strftime('%H:%M:%S')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Input Area
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input("Type your response...", key="user_input", label_visibility="collapsed")
        
        with col2:
            send_button = st.button("📤 Send", use_container_width=True, type="primary")
        
        if send_button and user_input:
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "time": datetime.now()
            })
            
            # Simulate AI thinking
            with st.spinner(f"{persona_name} is thinking..."):
                time.sleep(1.5)
                ai_response = generate_ai_response(persona_name, user_input)
                st.session_state.messages.append({
                    "role": "ai",
                    "content": ai_response,
                    "time": datetime.now()
                })
            
            st.rerun()
    
    # RESULTS SCREEN WITH AI ASSESSMENT
    elif st.session_state.session_complete:
        assessment = st.session_state.ai_assessment
        
        st.markdown('<div class="main-header">🤖 AI-Powered Performance Analysis</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub-header">Comprehensive assessment of your interaction with {st.session_state.selected_persona}</div>', unsafe_allow_html=True)
        
        # AI Insights Banner
        st.info("🤖 **AI Assessment:** This report was generated using advanced AI analysis of your conversation, evaluating multiple dimensions including content, delivery, and strategic approach.")
        
        # Overall Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            score_delta = assessment['overall_score'] - 80
            st.metric(label="Overall Score", value=assessment['overall_score'], delta=f"{score_delta:+d} vs baseline")
        
        with col2:
            session_length = len([m for m in st.session_state.messages if m['role'] == 'user'])
            st.metric(label="Conversation Depth", value=f"{session_length} exchanges", delta=None)
        
        with col3:
            skill_level = assessment['skill_level_update'].capitalize()
            st.metric(label="Skill Level", value=skill_level, delta=None)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # AI Insights Section
        if assessment['insights']:
            st.markdown("### 🎯 AI-Generated Insights")
            for insight in assessment['insights']:
                st.markdown(f"""
                <div style="background-color: #eff6ff; border-left: 4px solid #3b82f6; padding: 1rem; border-radius: 0.25rem; margin: 0.5rem 0;">
                    {insight}
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Performance Breakdown
        st.markdown("### 📈 Performance Breakdown")
        
        df_metrics = pd.DataFrame({
            'Category': list(assessment['category_scores'].keys()),
            'Your Score': list(assessment['category_scores'].values()),
            'Benchmark': [85, 80, 85, 80, 90]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Your Score',
            x=df_metrics['Category'],
            y=df_metrics['Your Score'],
            marker_color='#3b82f6'
        ))
        fig.add_trace(go.Bar(
            name='Benchmark',
            x=df_metrics['Category'],
            y=df_metrics['Benchmark'],
            marker_color='#9ca3af'
        ))
        
        fig.update_layout(
            barmode='group',
            height=400,
            xaxis_title="Competency Area",
            yaxis_title="Score (%)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Adaptive Learning Path Section
        if assessment['weak_areas']:
            st.markdown("### 📚 Recommended LMS Modules (Based on Weak Areas)")
            st.markdown(f"""
            <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 1rem; border-radius: 0.25rem; margin-bottom: 1rem;">
                <strong>⚠️ Development Areas Identified:</strong> {', '.join(assessment['weak_areas'])}<br>
                The AI has curated personalized learning content to help you improve in these areas.
            </div>
            """, unsafe_allow_html=True)
            
            for idx, module in enumerate(assessment['lms_recommendations']):
                priority_color = {
                    'High': '#ef4444',
                    'Medium': '#f59e0b',
                    'Low': '#10b981'
                }
                
                with st.expander(f"📖 {module['title']} ({module['type']}) - {module['duration']}", expanded=(idx == 0)):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Description:** {module['description']}")
                        st.markdown(f"**Priority:** <span style='color: {priority_color[module['priority']]};'>●</span> {module['priority']}", unsafe_allow_html=True)
                    
                    with col2:
                        if st.button(f"🔗 Access Module", key=f"lms_{idx}", use_container_width=True, type="primary"):
                            st.success(f"✅ Opening: {module['title']} (Demo mode)")
                            st.markdown(f"[Click here to access]({module['link']})")
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Advanced Scenario Recommendations
        if assessment['scenario_recommendations']:
            st.markdown("### 🚀 Next Challenge: Recommended Scenarios")
            
            if assessment['overall_score'] >= 88:
                st.markdown("""
                <div class="success-box">
                    <strong>🌟 Excellent Performance!</strong> You're ready for advanced scenarios. 
                    The AI recommends increasing complexity to continue your growth.
                </div>
                """, unsafe_allow_html=True)
            elif assessment['overall_score'] >= 80:
                st.markdown("""
                <div style="background-color: #dbeafe; border-left: 4px solid #3b82f6; padding: 1rem; border-radius: 0.25rem; margin-bottom: 1rem;">
                    <strong>💪 Strong Performance!</strong> You're ready for intermediate-advanced scenarios 
                    that will sharpen your skills further.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="warning-box">
                    <strong>📈 Building Foundation</strong> Focus on these scenarios to strengthen core competencies 
                    before moving to advanced challenges.
                </div>
                """, unsafe_allow_html=True)
            
            for idx, scenario in enumerate(assessment['scenario_recommendations']):
                difficulty_emoji = {
                    'Beginner-Intermediate': '🟢',
                    'Intermediate': '🟡',
                    'Intermediate-Advanced': '🟠',
                    'Advanced': '🔴',
                    'Expert': '🔴🔴'
                }
                
                st.markdown(f"""
                <div class="persona-card">
                    <h4>{difficulty_emoji.get(scenario['difficulty'], '🟡')} {scenario['title']}</h4>
                    <p><strong>Difficulty:</strong> {scenario['difficulty']} | <strong>Time:</strong> {scenario['estimated_time']}</p>
                    <p>{scenario['description']}</p>
                    <p><strong>Personas:</strong> {', '.join(scenario['personas'])}</p>
                    <p><strong>Skills Developed:</strong> {', '.join(scenario['skills_developed'])}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button(f"▶️ Start", key=f"scenario_{idx}", use_container_width=True):
                        st.success(f"✅ Launching: {scenario['title']} (Demo mode)")
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Strengths and Development Areas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Key Strengths")
            if assessment['strong_areas']:
                for area in assessment['strong_areas']:
                    st.markdown(f"""
                    <div class="success-box">
                        <strong>{area}</strong><br>
                        Excellent performance - maintain this strength
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="success-box">
                    <strong>Consistent Performance</strong><br>
                    Good baseline across all areas
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 🎯 Focus Areas")
            if assessment['weak_areas']:
                for area in assessment['weak_areas']:
                    st.markdown(f"""
                    <div class="warning-box">
                        <strong>{area}</strong><br>
                        Review recommended LMS modules above
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="success-box">
                    <strong>No Critical Gaps</strong><br>
                    Ready for advanced scenarios
                </div>
                """, unsafe_allow_html=True)
        
        # Manager Feedback
        st.markdown("### 💬 Manager's Coaching Notes")
        st.info("""
        **Great progress on building rapport with skeptical HCPs!** Your clinical knowledge is a real strength.
        
        **Focus area:** Work on preemptively addressing common objections before they're raised. Complete the recommended LMS modules this week and schedule a coaching session to practice advanced objection handling techniques.
        
        *- Sarah Johnson, Sales Manager*
        """)
        
        # Action Buttons
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📚 Go to LMS Dashboard", use_container_width=True, type="primary"):
                st.success("✅ Redirecting to Learning Management System... (Demo mode)")
        
        with col2:
            if st.button("🔄 Practice Another Scenario", use_container_width=True):
                st.session_state.session_complete = False
                st.session_state.selected_persona = None
                st.session_state.messages = []
                st.session_state.ai_assessment = None
                st.rerun()
        
        with col3:
            if st.button("🏠 Return to Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.session_state.session_complete = False
                st.session_state.selected_persona = None
                st.session_state.messages = []
                st.session_state.ai_assessment = None
                st.rerun()

# ANALYTICS PAGE
elif st.session_state.page == 'analytics':
    st.markdown('<div class="main-header">📊 Performance Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Track your progress and identify growth opportunities</div>', unsafe_allow_html=True)
    
    # Score Trend
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Score Trend (Last 8 Weeks)")
        trend_data = pd.DataFrame({
            'Week': ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8'],
            'Score': [72, 75, 78, 82, 85, 83, 86, 88]
        })
        
        fig_trend = px.line(trend_data, x='Week', y='Score', markers=True)
        fig_trend.update_traces(line_color='#3b82f6', line_width=3)
        fig_trend.update_layout(height=300, yaxis_range=[60, 100])
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Competency Radar")
        categories = ['Clinical', 'Rapport', 'Objections', 'Value', 'Compliance']
        values = [87, 92, 78, 85, 95]
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(59, 130, 246, 0.3)',
            line=dict(color='#3b82f6', width=2)
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    # Session History
    st.markdown("### 📋 Session History")
    
    history_data = pd.DataFrame({
        'Date': ['Jan 8, 2026', 'Jan 7, 2026', 'Jan 6, 2026', 'Jan 5, 2026', 'Jan 4, 2026'],
        'Persona': ['Dr. Chen', 'Dr. Roberts', 'Dr. Watson', 'Dr. Chen', 'Dr. Roberts'],
        'Scenario': ['Initial Introduction', 'Objection Handling', 'Competitor Comparison', 'Contract Negotiation', 'Initial Introduction'],
        'Duration': ['8:24', '12:15', '15:42', '11:30', '9:18'],
        'Score': [88, 85, 78, 82, 84],
        'Status': ['Completed', 'Completed', 'Completed', 'Completed', 'Completed']
    })
    
    st.dataframe(
        history_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score",
                help="Session score",
                format="%d%%",
                min_value=0,
                max_value=100,
            ),
        }
    )
    
    # Download Report
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📥 Download Full Performance Report", type="primary"):
        st.success("✅ Report downloaded successfully! (Demo mode)")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 1rem;">
    <p>AI Healthcare Coaching Platform • Demo Version • Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
