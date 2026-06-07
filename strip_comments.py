import tokenize
import os
import io

def strip_comments(filepath):
    with open(filepath, 'r') as f:
        source = f.read()

    # We use io.StringIO to create a file-like object for tokenize
    io_obj = io.StringIO(source)
    out = ""
    last_lineno = -1
    last_col = 0
    
    try:
        tokens = tokenize.generate_tokens(io_obj.readline)
        for tok in tokens:
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]
            
            if start_line > last_lineno:
                last_col = 0
            
            if start_col > last_col:
                out += (" " * (start_col - last_col))
                
            if token_type == tokenize.COMMENT:
                pass # Skip comments
            else:
                out += token_string
                
            last_lineno = end_line
            last_col = end_col
            
    except tokenize.TokenError:
        return False # Syntax error, don't touch
        
    with open(filepath, 'w') as f:
        f.write(out)
    return True

for f in os.listdir('.'):
    if f.endswith('.py') and f != 'strip_comments.py':
        strip_comments(f)
        print(f"Stripped comments from {f}")

