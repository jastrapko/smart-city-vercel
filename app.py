# app.py (Revised Version)

from flask import Flask, render_template, request, session, redirect, url_for
import textwrap

# REVISED >> Feature list updated with new items and descriptions
FEATURES = [
    # Essential Infrastructure
    {'id': 'E1', 'name': 'Smart Grid', 'category': 'Essential Infrastructure', 'cost': 350, 'description': 'A modern electricity grid for reliable, efficient power distribution. Foundational for many advanced systems.', 'prereqs': []},
    {'id': 'E2', 'name': 'Integrated Water Management', 'category': 'Essential Infrastructure', 'cost': 300, 'description': 'Smart sensors and systems to monitor water quality, prevent leaks, and manage distribution.', 'prereqs': []},
    {'id': 'E3', 'name': 'Multi-Modal Transit Network', 'category': 'Essential Infrastructure', 'cost': 400, 'description': 'Connects buses, trains, and bike shares into a single, efficient public transport system.', 'prereqs': []},
    {'id': 'E4', 'name': 'Automated Waste Management', 'category': 'Essential Infrastructure', 'cost': 250, 'description': 'Smart bins that signal when they are full, optimizing collection routes and reducing fuel usage.', 'prereqs': []},

    # Sustainability Systems
    {'id': 'S1', 'name': 'Utility-Scale Solar Farm', 'category': 'Sustainability Systems', 'cost': 350, 'description': 'Large-scale solar panel installation to provide clean energy to the city.', 'prereqs': ['E1']},
    {'id': 'S2', 'name': 'Green Building Mandates', 'category': 'Sustainability Systems', 'cost': 200, 'description': 'Policies requiring new constructions to be energy-efficient and use sustainable materials.', 'prereqs': []},
    {'id': 'S3', 'name': 'City-Wide EV Charging Network', 'category': 'Sustainability Systems', 'cost': 250, 'description': 'Extensive network of public charging stations for electric vehicles.', 'prereqs': ['E1']},
    {'id': 'S4', 'name': 'Advanced Recycling & Composting Program', 'category': 'Sustainability Systems', 'cost': 150, 'description': 'Diverts a significant portion of waste from landfills, creating a circular economy.', 'prereqs': ['E4']},
    {'id': 'S5', 'name': 'Urban Farming Initiatives', 'category': 'Sustainability Systems', 'cost': 180, 'description': 'Provides grants and land-use variances for vertical farms and community gardens. Increases local food security, reduces food transportation miles, and provides green spaces.', 'prereqs': []},
    {'id': 'S6', 'name': 'Kinetic Roadway Generators', 'category': 'Sustainability Systems', 'cost': 300, 'description': 'Installs piezoelectric generators under major roadways to capture the energy of passing vehicles, supplementing the main power grid.', 'prereqs': ['E1']},

    # Quality of Life
    {'id': 'Q1', 'name': 'Public WiFi', 'category': 'Quality of Life', 'cost': 150, 'description': 'Provides free public internet access. Consider the trade-offs: A city-run network is costly, while a corporate-sponsored one may raise data privacy concerns for your citizens.', 'prereqs': []},
    {'id': 'Q2', 'name': 'Smart Parks & Recreation', 'category': 'Quality of Life', 'cost': 120, 'description': 'Parks with smart irrigation, interactive installations, and digital booking for facilities.', 'prereqs': []},
    {'id': 'Q3', 'name': 'Telehealth & Digital Healthcare', 'category': 'Quality of Life', 'cost': 280, 'description': 'Infrastructure for remote doctor consultations and digital health record management.', 'prereqs': []},
    {'id': 'Q4', 'name': 'Digital Education Platform', 'category': 'Quality of Life', 'cost': 220, 'description': 'Connects schools, libraries, and students with online learning resources and tools.', 'prereqs': []},
    {'id': 'Q5', 'name': 'Open Data & Civic Tech Hub', 'category': 'Quality of Life', 'cost': 180, 'description': 'Promotes transparency and citizen engagement by making city data public and accessible.', 'prereqs': []},
    {'id': 'Q6', 'name': 'Citizen Reporting App', 'category': 'Quality of Life', 'cost': 100, 'description': 'A mobile app allowing residents to report issues like potholes, broken streetlights, and graffiti directly to municipal services. A great first step in building civic trust and engagement.', 'prereqs': []},

    # Advanced Technology
    {'id': 'A1', 'name': 'AI-Powered Traffic Management', 'category': 'Advanced Technology', 'cost': 450, 'description': 'Uses AI to analyze traffic flow in real-time, adjusting traffic lights to reduce congestion.', 'prereqs': ['E1', 'E3']},
    {'id': 'A2', 'name': 'IoT Smart Street Lighting', 'category': 'Advanced Technology', 'cost': 300, 'description': 'LED lights that adjust brightness based on real-time activity, saving energy and improving safety.', 'prereqs': ['E1']},
    {'id': 'A3', 'name': 'City-Scale Environmental Monitoring', 'category': 'Advanced Technology', 'cost': 320, 'description': 'Network of sensors to monitor air quality, noise levels, and other environmental factors.', 'prereqs': ['E1']},
    {'id': 'A4', 'name': 'Drone-Based Services (Delivery/Inspection)', 'category': 'Advanced Technology', 'cost': 350, 'description': 'Infrastructure and regulations for using drones for package delivery and infrastructure inspection.', 'prereqs': ['E1']},
    {'id': 'A5', 'name': 'Predictive Policing AI', 'category': 'Advanced Technology', 'cost': 450, 'description': 'An expensive AI system that analyzes historical crime data to forecast hotspots and allocate police resources. Proponents claim it reduces crime, but critics warn it can entrench and legitimize historical biases. A powerful but controversial choice.', 'prereqs': []},
    {'id': 'A6', 'name': 'City Digital Twin Platform', 'category': 'Advanced Technology', 'cost': 500, 'description': 'A comprehensive, real-time 3D model of the entire city, integrating data from all other smart systems. A powerful tool for simulation and planning, but requires significant investment in other data-producing systems to be useful.', 'prereqs': ['E1', 'A3']},
]
FEATURE_MAP = {f['id']: f for f in FEATURES}
CATEGORIES = sorted(list(set(f['category'] for f in FEATURES)))
# REVISED >> Budget is now 1100
INITIAL_BUDGET = 1100

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-smart-city'

def calculate_score(selections):
    # This scoring logic remains the same and does not need to be changed.
    score, strengths, weaknesses, recommendations = 0, [], [], []
    selected_ids = selections.keys()
    
    costs = {cat: 0 for cat in CATEGORIES}
    for feature in selections.values():
        costs[feature['category']] += feature['cost']
    total_cost = sum(costs.values())

    if costs.get('Essential Infrastructure', 0) == 0:
        score -= 200
        weaknesses.append("CRITICAL: The city lacks any essential infrastructure.")
        recommendations.append("Invest in 'Essential Infrastructure' like Smart Grid (E1).")
    else:
        score += 100
        strengths.append("STRONG FOUNDATION: Built on essential infrastructure.")

    core_categories = ['Essential Infrastructure', 'Sustainability Systems', 'Quality of Life']
    core_spending_count = sum(1 for cat in core_categories if costs.get(cat, 0) > 0)
    if core_spending_count < 3 and total_cost > 0:
        weaknesses.append("IMBALANCED FOCUS: Neglects core areas like Sustainability or Quality of Life.")
        recommendations.append("Balance investment across Infrastructure, Sustainability, and Quality of Life.")
    elif core_spending_count == 3:
        score += 150
        strengths.append("BALANCED DEVELOPMENT: Excellent balance across core areas.")
        
    prereq_bonus = 0
    for feature in selections.values():
        if all(prereq_id in selected_ids for prereq_id in feature['prereqs']):
            prereq_bonus += 30
        else:
            missing = [p for p in feature['prereqs'] if p not in selected_ids]
            if missing:
                weaknesses.append(f"INEFFICIENT TECH: '{feature['name']}' is missing prerequisites ({', '.join(missing)}).")
    if prereq_bonus > 0:
        score += prereq_bonus
        strengths.append("SYNERGY: Correctly sequenced technology for maximum effect.")

    if total_cost > INITIAL_BUDGET * 0.9:
        score += 50
        strengths.append("EFFICIENT BUDGETING: Used the budget effectively.")
    elif total_cost < INITIAL_BUDGET * 0.5 and total_cost > 0:
        weaknesses.append("UNDERSPENDING: Significant budget remains, indicating missed opportunities.")

    if score > 200: viability = "Very High. A balanced, sustainable, and functional city."
    elif score > 100: viability = "High. A strong plan with solid foundations."
    elif score > 0: viability = "Moderate. Has potential but suffers from imbalances."
    else: viability = "Low. Critical flaws will likely lead to systemic issues."

    return {
        "score": score, "strengths": list(set(strengths)), "weaknesses": list(set(weaknesses)),
        "recommendations": list(set(recommendations)), "viability": viability,
        "costs_by_category": costs, "total_cost": total_cost,
    }

@app.route('/', methods=['GET', 'POST'])
def game():
    if 'selections' not in session:
        session['selections'] = {}
        session['budget'] = INITIAL_BUDGET
        session['report'] = None

    if request.method == 'POST':
        action = request.form.get('action')
        feature_id = request.form.get('feature_id')

        if action == 'add' and feature_id in FEATURE_MAP:
            feature = FEATURE_MAP[feature_id]
            if feature['cost'] <= session['budget'] and feature_id not in session['selections']:
                session['budget'] -= feature['cost']
                selections = session['selections'].copy()
                selections[feature_id] = feature
                session['selections'] = selections
        elif action == 'remove' and feature_id in session['selections']:
            feature = session['selections'][feature_id]
            session['budget'] += feature['cost']
            selections = session['selections'].copy()
            del selections[feature_id]
            session['selections'] = selections
        elif action == 'finalize':
            session['report'] = calculate_score(session['selections'])
        
        return redirect(url_for('game'))

    available_features = sorted([f for f in FEATURES if f['id'] not in session['selections']], key=lambda x: x['id'])
    selected_features = sorted(session['selections'].values(), key=lambda x: x['id'])
    
    return render_template('index.html', 
                           budget=session['budget'],
                           selections=selected_features,
                           available_features=available_features,
                           categories=CATEGORIES,
                           report=session['report'])

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('game'))

if __name__ == "__main__":
    app.run(debug=True)
