import os
import re
from github import Github

# Conexão segura usando o Token do GitHub Actions
token = os.getenv('GITHUB_TOKEN')
g = Github(token)
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))

# 1. Lógica do Contador
if not os.path.exists("count.txt"):
    with open("count.txt", "w") as f: f.write("0")

with open("count.txt", "r+") as f:
    current_count = int(f.read().strip()) + 1
    f.seek(0)
    f.write(str(current_count))
    f.truncate()

# 2. Lógica do Mural (Busca as Issues com o título específico)
issues = repo.get_issues(state='open')
comments_list = []
for issue in issues:
    if "Mensagem para o Mural" in issue.title:
        # Formata o comentário: Nome do usuário e o que ele escreveu
        comments_list.append(f"<li><b>{issue.user.login}:</b> {issue.body}</li>")

# Mantém apenas os 5 comentários mais recentes
comments_html = "\n".join(comments_list[:5])

# 3. Atualização do README.md
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Atualiza o Badge de Visitantes via Regex
content = re.sub(r'Visitante%20n%C2%BA-\d+-blue', f'Visitante%20n%C2%BA-{current_count}-blue', content)

# Atualiza a seção do Mural entre as tags de âncora
marker_start = ""
marker_end = ""

if comments_html:
    replacement = f"{marker_start}\n<ul>\n{comments_html}\n</ul>\n{marker_end}"
else:
    replacement = f"{marker_start}\n*Ainda não há comentários. Seja o primeiro!*\n{marker_end}"

new_content = re.sub(f"{marker_start}.*?{marker_end}", replacement, content, flags=re.DOTALL)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)
  
