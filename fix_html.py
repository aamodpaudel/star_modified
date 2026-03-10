import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Grid Cols
    content = content.replace('grid-cols-1 md:grid-cols-2 lg:grid-cols-4', 'grid-cols-1 md:grid-cols-3 lg:grid-cols-3')
    
    # Category 1: 30% -> 40%
    cat1_pattern = r'(<!-- Category 1 -->.*?<span class="text-brand font-black text-2xl">)30%(</span>)'
    content = re.sub(cat1_pattern, r'\g<1>40%\g<2>', content, flags=re.DOTALL)
    
    # Category 2: 10% -> 30%
    cat2_pattern = r'(<!-- Category 2 -->.*?<span class="text-brand font-black text-2xl">)10%(</span>)'
    content = re.sub(cat2_pattern, r'\g<1>30%\g<2>', content, flags=re.DOTALL)
    
    # Category 4 removal
    # We match exactly the category 4 div block which ends with "</div>" (there are nested elements)
    cat4_pattern = r'<!-- Category 4 -->\s*<div class="p-5 border border-slate-200 bg-slate-50 rounded-2xl flex flex-col gap-4">\s*<p class="text-slate-800 text-xs font-bold uppercase tracking-wider">STAR Circle\s*Engagement</p>\s*<span class="text-brand font-black text-2xl">30%</span>\s*<p class="text-\[10px\] text-slate-600 leading-relaxed capitalize">what was the\s*engagement &amp; responsiveness rate evaluated by circle leaders for the\s*participants from a\s*certain university</p>\s*</div>'
    content = re.sub(cat4_pattern, '', content)
    
    # Remove STAR Circle Engagement TH
    # In index.html: <th class="... relative group">\s*STAR Circle Engagement.*?</div>\s*</th>
    # In rankings.html: <th class="...">\s*STAR Circle Engagement\s*</th>
    th_pattern1 = r'<th class="px-6 py-4 font-bold uppercase text-slate-500 tracking-widest text-right">\s*STAR Circle Engagement\s*</th>'
    content = re.sub(th_pattern1, '', content)
    
    th_pattern2 = r'<th class="px-6 py-3 text-\[10px\] font-bold uppercase text-slate-500 tracking-widest text-right relative group">\s*STAR Circle Engagement\s*<div[^>]*>.*?</div>\s*</th>'
    content = re.sub(th_pattern2, '', content, flags=re.DOTALL)
    
    # Remove TD with percentage
    # Just remove `\n<td class="... text-right text-slate-600">...%</td>` from the rows
    content = re.sub(r'\s*<td class="px-6 py-4 text-right text-slate-600">\s*\d+%\s*</td>', '', content)
    
    # Fix Whitespace
    content = content.replace('pt-16 pb-24 px-6 border-b border-slate-200', 'pt-16 pb-12 px-6 border-b border-slate-200')
    content = content.replace('pt-32 pb-16 px-6" id="upcoming-circles"', 'pt-24 pb-16 px-6" id="upcoming-circles"')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

process_file('d:/0_Github_Repos/2026_star/index.html')
process_file('d:/0_Github_Repos/2026_star/rankings.html')
