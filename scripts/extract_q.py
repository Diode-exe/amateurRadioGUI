from bs4 import BeautifulSoup

def extract_q_codes(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    q_codes = {}
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 3:
            code = cells[0].get_text(strip=True)
            question = cells[1].get_text(strip=True)
            answer = cells[2].get_text(strip=True)
            q_codes[code] = {"question": question, "answer": answer}
    
    return q_codes

print(extract_q_codes("q-codes.html"))
with open("q_codes_extracted.txt", "w", encoding="utf-8") as f:
    for code, qa in extract_q_codes("q-codes.html").items():
        f.write(f"{{'{code}': '{qa['question']} - {qa['answer']}'}},\n")