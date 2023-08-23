def extract_image_links(image_links):
    image_links_list = []
    current_link = ""

    for char in image_links:
        if char == "\n":
            if current_link:
                image_links_list.append(current_link.strip(";"))
            current_link = ""
        else:
            current_link += char

    if current_link:
        image_links_list.append(current_link.strip(";"))

    return image_links_list

def time_util(start_time,end_time):
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")