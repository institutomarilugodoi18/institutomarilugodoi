# Backlog / Pendências (ONG)

## UX / Navegação
- [ ] Voluntários: deixar rolagem só nas linhas da tabela e cabeçalho fixo (sticky thead)
- [ ] Voluntários: reposicionar botões (Painel/Início/Sair) no topo (e opcional no rodapé)
- [ ] Padronizar saudação ("Olá, ...") e botão Sair: mover para navbar/base (definir padrão)
- [ ] Padronizar listas internas (Voluntários e Animais): mesma barra superior (Painel/Relatórios/Sair + Olá usuário) e botões de ação no topo
- [ ] Animais: ajustar ordem de colunas, formatar datas e adicionar ações (Editar/Excluir) + confirmação de exclusão
- [ ] Voluntários: mover “Voltar” para Painel e Início para uma barra fixa (topo) e revisar o “Olá, admin!” (padronizar com Painel)

## URLs / Namespaces
- [ ] Padronizar namespace do app voluntarios (app_name + include com namespace)
- [ ] Atualizar templates/reverse() para usar `voluntarios:...` sem quebrar links

## Painel / Relatórios
- [ ] Criar rota /relatorios/ e card “Relatórios” no painel apontando para ela
- [ ] Definir quais métricas vão entrar no dashboard (animais + voluntários)

## Animais
- [ ] Criar model Animal + admin + migration
- [ ] CRUD completo (list/create/update/delete)
- [ ] Upload de foto (MEDIA_URL/MEDIA_ROOT)
- [ ] Otimização/compressão de imagem (Pillow) e limite de tamanho (ex.: ~300KB)
- [ ] Dashboard de métricas + gráficos (Chart.js)
- [ ] Produção (Brasil Cloud): configurar persistência/armazenamento de uploads (MEDIA_ROOT) e servir `/media/` (nginx/painel)
- [ ] Remover `urlpatterns += static(...)` do `urls.py` após media em produção estar OK