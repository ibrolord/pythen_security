import os, glob, sys, re, docx

pattern = ".docx"
dir_path = "/x/processes"


# list tru dir recusively 
def list_dir(pattern, dir_path):
    files = []
    if not os.path.isdir(dir_path):
        pwd = os.getcwd()
        print(f"[-] {dir_path} does not exist in {pwd}")
        sys.exit(1)
    
    for file in glob.glob(dir_path + f'/**/*{pattern}', recursive=True):
        file = file.split('/')[-1]
        # print(file)
        files.append(file)
    return files





# open each file
def open_file(files, dir_path):
    for file in files:
        full_path = f'{dir_path}/{file}'
        # print(full_path)
        doc = docx.Document(full_path)
        # print(file)

        if 'Solis' in file:
            # os.rename(full_path, file.replace('Solis',''))
            new_name = file.replace('zz','xx')
            os.rename(full_path,f'{dir_path}/{new_name}')
            os.remove(file)

        
        for paragraph in doc.paragraphs:
            # print(paragraph.text)
            if "Solis" in paragraph.text:
                paragraph.text = paragraph.text.replace("zz", "xx")
                print(paragraph.text)

        doc.save(full_path)


if __name__ == '__main__':
    file = list_dir(pattern, dir_path)
    # print(file)
    open_file(file, dir_path)
    