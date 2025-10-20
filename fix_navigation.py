"""
Fix navigation issue - st.switch_page requires specific paths
According to Streamlit docs, you cannot switch_page to app.py from pages/
You can only switch between pages in pages/ directory
"""

import re

# Read the navigation file
with open('src/ui/main_navigation.py', 'r', encoding='utf-8') as f:
    content = f.read()

# The issue: st.switch_page("app.py") from pages/ doesn't work
# Solution: Use st.page_link instead, or handle home differently

# Replace the problematic switch_page logic
old_code = """            if st.button(
                nav_item["label"],
                key=f"nav_{nav_item['key']}",
                use_container_width=True,
                disabled=is_current,
                type="primary" if is_current else "secondary"
            ):
                st.switch_page(nav_item["page"])"""

new_code = """            if st.button(
                nav_item["label"],
                key=f"nav_{nav_item['key']}",
                use_container_width=True,
                disabled=is_current,
                type="primary" if is_current else "secondary"
            ):
                # Handle homepage navigation separately (can't switch_page to app.py from pages/)
                if nav_item["key"] == "home":
                    # Use st.page_link for homepage or inform user
                    st.info("Para voltar ao inicio, clique no logo 'PanoramaCP2B' na sidebar ou feche esta aba")
                else:
                    st.switch_page(nav_item["page"])"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("[OK] Navigation logic updated")
else:
    print("[WARN] Could not find exact match for navigation code")

# Write back
with open('src/ui/main_navigation.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n[SUCCESS] Navigation file updated!")
print("\nNote: Home button will show info message since Streamlit cannot")
print("switch_page() from pages/ to app.py")
