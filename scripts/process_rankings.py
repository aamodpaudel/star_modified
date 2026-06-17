import csv
from datetime import datetime
import json
import math

def normalize_institution(name):
    name = name.strip()
    # Remove extra spaces and common noise
    name = ' '.join(name.split())
    name_lower = name.lower()
    
    # Specific common consolidations
    if any(x in name_lower for x in ['kathmandu university', 'ku school', 'kusoe']):
        return 'Kathmandu University'
    if any(x in name_lower for x in ['tribhuvan university', 'tribhuwan university', 'central department of economics', 'institute of engineering (ioe)']):
        return 'Tribhuvan University'
    if 'morgan state university' in name_lower:
        return 'Morgan State University'
    if 'op jindal' in name_lower or 'o.p. jindal' in name_lower or 'jindal global' in name_lower:
        return 'O.P. Jindal Global University'
    if 'american university in the emirates' in name_lower or 'aue' == name_lower:
        return 'American University in the Emirates'
    if 'university of algiers' in name_lower:
        return 'University of Algiers'
    if any(x in name_lower for x in ['nepal open university', 'nou']):
        return 'Nepal Open University'
    if 'musashino university' in name_lower:
        return 'Musashino University'
    if 'far western university' in name_lower:
        return 'Far Western University'
    if 'michigan state university' in name_lower:
        return 'Michigan State University'
    if 'istanbul aydin university' in name_lower:
        return 'Istanbul Aydin University'
    if 'federal university wukari' in name_lower:
        return 'Federal University Wukari'
    if 'saarland university' in name_lower:
        return 'Saarland University of Applied Sciences'
    if 'masinde muliro university' in name_lower:
        return 'Masinde Muliro University'
    if 'northwestern university' in name_lower:
        return 'Northwestern University'
    
    return name

def process_rankings(csv_path):
    institutions = {}
    current_year = datetime.now().year

    # List of entities to explicitly remove as per user request
    explicit_remove = [
        'sagacia jewelry', 'aeonfly', 'world health organization', 'dumpsboss', 
        'mystudy education consulting', 'ctspoint', 'the student helpline', 
        'vibrant finance', 'ascent innovations', 'ministry of education', 
        'moselewapula junior secondary school', 'organization', 'volunteer at star scholars network'
    ]
    
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_inst = row.get('Institution', '').strip()
            
            # Basic validation
            if not raw_inst or raw_inst.lower() in ['unknown', 'not specified', 'na', 'n/a', 'unknown (not specified)', 'not applicable', 'none', 'nil']:
                continue
            
            if len(raw_inst) > 120:
                continue

            # Heuristic: if it has common title words or is a personal status phrase
            # Even if it contains "University", these are likely personal records
            title_exclusion_words = [
                'professor', 'teacher', 'manager', 'consultant', 'associate', 'advisor', 
                'researcher', 'engineer', 'student', 'studying', 'msc', 'phd', 'candidate', 
                'lecturer', 'faculty', 'scholar', 'fellow', 'applicant', 'nominee'
            ]
            
            raw_inst_lower = raw_inst.lower()
            if any(tw in raw_inst_lower for tw in title_exclusion_words):
                # Exception: if it's a "Department of...", "Faculty of..." it might be okay, 
                # but "Associate Professor at..." should be excluded.
                # However, the user wants "University", so let's be strict.
                if 'university' in raw_inst_lower:
                    # check if the word "university" is part of a longer phrase like "studying at University"
                    if any(x in raw_inst_lower for x in ['studying', 'professor', 'lecturer']):
                        continue

            inst = normalize_institution(raw_inst)
            inst_lower = inst.lower()

            # Apply explicit removals
            if any(rem in inst_lower for rem in explicit_remove):
                continue

            # CRITICAL: Only add institutions that have "university" in their name
            if 'university' not in inst_lower:
                continue

            if inst not in institutions:
                institutions[inst] = {
                    'members': 0,
                    'authentic': 0,
                    'total_seniority_years': 0,
                    'sum_of_join_years': 0,
                    'countries': set(),
                    'advanced': 0,
                    'fields': set(),
                    'primary_country': row.get('Country', 'Unknown')
                }
            
            data = institutions[inst]
            data['members'] += 1
            
            if row.get('Agent Review') == 'AUTHENTIC':
                data['authentic'] += 1
            
            created_at = row.get('Created At', '')
            if created_at:
                try:
                    year = datetime.strptime(created_at.split(' ')[0], '%Y-%m-%d').year
                    data['total_seniority_years'] += (current_year - year + 1)
                    data['sum_of_join_years'] += year
                except:
                    pass
            
            country = row.get('Country', '').strip()
            if country:
                data['countries'].add(country)
            
            career_stage = row.get('Career Stage', '')
            if 'Advanced' in career_stage:
                data['advanced'] += 1
            
            field = row.get('Professional Field', '').strip()
            if field:
                data['fields'].add(field)

    results = []
    for inst, data in institutions.items():
        results.append({
            'institution': inst,
            'members': data['members'],
            'authentic': data['authentic'],
            'total_seniority': data['total_seniority_years'],
            'avg_join_year': round(data['sum_of_join_years'] / data['members']) if data['members'] else 0,
            'countries_count': len(data['countries']),
            'advanced': data['advanced'],
            'fields_count': len(data['fields']),
            'country': data['primary_country'],
            'circles_led': math.ceil(data['members'] / 10)
        })

    if not results:
        return []

    # Normalization and Scoring
    max_vals = {
        'members': max(r['members'] for r in results) or 1,
        'authentic': max(r['authentic'] for r in results) or 1,
        'total_seniority': max(r['total_seniority'] for r in results) or 1,
        'countries_count': max(r['countries_count'] for r in results) or 1,
        'advanced': max(r['advanced'] for r in results) or 1,
        'fields_count': max(r['fields_count'] for r in results) or 1
    }

    for r in results:
        # Raw weighted score
        raw_score = (
            (r['members'] / max_vals['members']) * 25 +
            (r['authentic'] / max_vals['authentic']) * 25 +
            (r['total_seniority'] / max_vals['total_seniority']) * 15 +
            (r['countries_count'] / max_vals['countries_count']) * 10 +
            (r['advanced'] / max_vals['advanced']) * 15 +
            (r['fields_count'] / max_vals['fields_count']) * 10
        )
        r['raw_score'] = raw_score

    for r in results:
        # Raw weighted score (absolute out of 100)
        score_out_of_100 = (
            (r['members'] / max_vals['members']) * 25 +
            (r['authentic'] / max_vals['authentic']) * 25 +
            (r['total_seniority'] / max_vals['total_seniority']) * 15 +
            (r['countries_count'] / max_vals['countries_count']) * 10 +
            (r['advanced'] / max_vals['advanced']) * 15 +
            (r['fields_count'] / max_vals['fields_count']) * 10
        )
        # Scale to 10.0
        r['score'] = round(score_out_of_100 / 10, 1)
        
        # Diversity Index Logic
        if r['fields_count'] >= 6: r['diversity_index'] = "Very High"
        elif r['fields_count'] >= 3: r['diversity_index'] = "High"
        else: r['diversity_index'] = "Moderate"

        # Tier calculation for UI badges (adjusted for 10-point scale)
        if r['score'] >= 9.0: r['tier'] = "Platinum"
        elif r['score'] >= 7.0: r['tier'] = "Gold"
        elif r['score'] >= 4.0: r['tier'] = "Silver"
        else: r['tier'] = "Bronze"

    # Sort by raw score for precision
    results.sort(key=lambda x: x['raw_score'], reverse=True)
    return results # Return all for now, slicing will happen if needed or in export

if __name__ == '__main__':
    top_50 = process_rankings('D:/2026_star/STAR Scholars Network-members.csv')
    with open('rankings_data.json', 'w') as f:
        json.dump(top_50, f, indent=4)
    print("Top 10 Consolidated Institutions:")
    for i, r in enumerate(top_50[:10], 1):
        print(f"{i}. {r['institution']} - Score: {r['score']}% - Members: {r['members']} - Circles: {r['circles_led']}")
