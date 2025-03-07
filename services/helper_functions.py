'''
Converts a list of strings into a single string where the strings in the list are presented in bullet point form.

Parameters:
    - original_list: List of strings to be converted into bullet points
    - output: Final string with the original strings in the list presented in bullet point form

'''
def convert_list_to_bullet_points(original_list):
    output = "\n- ".join(original_list)
    return "- " + output