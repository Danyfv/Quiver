import re
from .executor import execute_command

def process_replacements(text, replace_config):
    """
    Scans text for tags defined in replace_config and replaces them
    with the output of the corresponding command.
    """
    if not text or not replace_config:
        return text

    # Create a regex pattern for all keys
    # Escaping keys just in case they contain special regex chars
    sorted_keys = sorted(replace_config.keys(), key=len, reverse=True)
    if not sorted_keys:
        return text
        
    pattern = re.compile("|".join(map(re.escape, sorted_keys)))
    
    def replace_match(match):
        tag = match.group(0)
        item = replace_config.get(tag)
        if item:
            success, output = execute_command(item)
            if success:
                return output
            else:
                return f"[Error: {output}]"
        return tag

    return pattern.sub(replace_match, text)
