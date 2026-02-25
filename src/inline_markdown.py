import re

from src.textnode import TextNode, TextType
from rich import print


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    # Lista, w której zapiszemy przetworzone węzły
    result_list = []

    for old_node in old_nodes:
        # Jeśli węzeł nie jest czystym tekstem, pomijamy go i dodajemy bez zmian
        if old_node.text_type != TextType.TEXT:
            result_list.append(old_node)
            continue

        # Wyciągamy listę obrazków (alt text i url) z tekstu węzła
        extracted_markdown_images = extract_markdown_images(old_node.text)

        # Jeśli nie znaleziono obrazków, dodajemy węzeł w całości
        if not extracted_markdown_images:
            result_list.append(old_node)
            continue

        # Zmienna pomocnicza do śledzenia pozostałego tekstu do przetworzenia
        current_text = old_node.text

        for image_details in extracted_markdown_images:
            # Dzielimy tekst na dwie części: przed obrazkiem i po obrazku
            result_of_split = current_text.split(f"![{image_details[0]}]({image_details[1]})", 1)
            # Aktualizujemy pozostały tekst do dalszej analizy
            current_text = result_of_split[1]

            # Jeśli przed obrazkiem był jakiś tekst, dodajemy go jako węzeł tekstowy
            if result_of_split[0]:
                result_list.append(TextNode(result_of_split[0], TextType.TEXT))

            # Dodajemy sam obrazek jako nowy węzeł typu IMAGE
            result_list.append(TextNode(image_details[0], TextType.IMAGE, image_details[1]))

        # Jeśli po ostatnim obrazku został jeszcze jakiś tekst, dodajemy go na koniec
        if current_text:
            result_list.append(TextNode(current_text, TextType.TEXT))

    return result_list


def split_nodes_link(old_nodes):
    # Lista na przetworzone węzły
    result_list = []

    for old_node in old_nodes:
        # Jeśli węzeł nie jest tekstem, dodaj go bez zmian
        if old_node.text_type != TextType.TEXT:
            result_list.append(old_node)
            continue

        # Wyciągnij wszystkie linki z tekstu
        extracted_markdown_links = extract_markdown_links(old_node.text)

        # Jeśli nie ma linków, dodaj cały węzeł i idź dalej
        if not extracted_markdown_links:
            result_list.append(old_node)
            continue

        # Tekst, który pozostał do podzielenia
        current_text = old_node.text

        for link_details in extracted_markdown_links:
            # Podziel tekst na części używając linku jako separatora (tylko pierwsze wystąpienie)
            result_of_split = current_text.split(f"[{link_details[0]}]({link_details[1]})", 1)
            # Zachowaj resztę tekstu do dalszego sprawdzania tj. druga część [1] zawierająca niepodzielony jeszcze tekst
            current_text = result_of_split[1]

            # Jeśli przed linkiem był tekst, dodaj go jako zwykły węzeł
            if result_of_split[0]:
                result_list.append(TextNode(result_of_split[0], TextType.TEXT))

            # Dodaj sam link jako węzeł typu LINK
            result_list.append(TextNode(link_details[0], TextType.LINK, link_details[1]))

        # Jeśli po wszystkich linkach został tekst, dodaj go na koniec
        if current_text:
            result_list.append(TextNode(current_text, TextType.TEXT))

    # Zwróć nową listę węzłów
    return result_list


def text_to_textnodes(text):
    # Tworzy początkową listę z jednym węzłem tekstowym
    result = [TextNode(text, TextType.TEXT)]
    # Wyodrębnia obrazki oraz linki (zaczynamy od tego na wypadek gdyby split_nodes_delimiter próbował rozbijać te bloki)
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    # Kolejno dzieli tekst na podstawie znaczników markdown
    result = split_nodes_delimiter(result, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    return result
