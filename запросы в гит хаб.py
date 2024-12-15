import requests
import json

# Функция для поиска репозиториев на GitHub
def search_github_repositories(query, per_page=10):
    url = "https://api.github.com/search/repositories"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Python Script",
        # Если есть токен, добавьте его сюда для повышения лимита запросов
        # "Authorization": "token YOUR_GITHUB_TOKEN"
    }
    params = {
        "q": query,
        "per_page": per_page,
        "sort": "stars",
        "order": "desc",
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")
        return []

# Вычисление схожести запросов на основе совпадения слов
from collections import Counter

def calculate_similarity(query, description):
    query_words = Counter(query.lower().split())
    description_words = Counter(description.lower().split())
    common_words = query_words & description_words
    similarity = sum(common_words.values()) / max(len(query_words), 1)
    return similarity

# Основная программа
def main():
    # Ввод запроса от пользователя
    user_query = input("Введите ключевой запрос для поиска: ")

    # Поиск репозиториев на GitHub
    print("Поиск репозиториев на GitHub...")
    github_results = search_github_repositories(user_query, per_page=50)

    if not github_results:
        print("Не удалось найти подходящих репозиториев.")
        return

    # Сравнение введенного запроса с описаниями репозиториев
    results_with_similarity = []
    for repo in github_results:
        description = repo['description'] or ""
        similarity = calculate_similarity(user_query, description)
        results_with_similarity.append((repo, similarity))

    # Сортировка результатов по степени сходства
    sorted_results = sorted(results_with_similarity, key=lambda x: x[1], reverse=True)

    # Запись результатов в файл
    with open("github_repositories.txt", "w", encoding="utf-8") as file:
        for repo, similarity in sorted_results[:10]:
            file.write(f"Тема: {repo['name']}\n")
            file.write(f"Описание: {repo['description']}\n")
            file.write(f"Ссылка: {repo['html_url']}\n")
            file.write(f"Сходство: {similarity:.4f}\n\n")

    print("Результаты сохранены в файл github_repositories.txt")

if __name__ == "__main__":
    main()
