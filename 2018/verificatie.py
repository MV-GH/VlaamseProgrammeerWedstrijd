import difflib
import subprocess


def verify(solution, input, output, subpath=""):
    solution = subpath + solution
    input = subpath + input
    output = subpath + output

    test = subprocess.run(['python', solution], stdin=open(input), stdout=subprocess.PIPE, text=True)

    with open(output) as file_2:
        output_text = file_2.readlines()
    output_text[-1] += '\n'  # missing the last newline in all my outputs somehowe

    diffs = difflib.unified_diff(test.stdout.splitlines(True), output_text, fromfile=input, tofile=output, lineterm='')

    success = True
    for line in diffs:
        success = False
        print(repr(line))  # prevent escape chars from working

    if success:
        print(f"{input} matched {output} \n 🚀 SUCCESS 👍 🚀")


#verify("oplossing.py", "vb.invoer", "vb.uitvoer", "bergwandel/")
#verify("oplossing.py", "wedstrijd.invoer", "wedstrijd.uitvoer", "bergwandel/")
verify("oplossing.py", "vb.invoer", "vb.uitvoer", "slinger/")
verify("oplossing.py", "wedstrijd.invoer", "wedstrijd.uitvoer", "slinger/")