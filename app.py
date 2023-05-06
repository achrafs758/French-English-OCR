import streamlit as st
import pdf2image
import pytesseract
from pytesseract import Output, TesseractError
from ocr_functions import convert_pdf_to_txt_pages, convert_pdf_to_txt_file, save_pages, displayPDF, images_to_txt

st.set_page_config(page_title="French-English OCR")


html_temp = """
            <div style="background-color:{};padding:1px">
            
            </div>
            """
st.markdown("# Image-to-Text Converter For French and English documents")
st.markdown(
        "This application is used to convert a PDF or image that has **French or English** text (scanned or otherwise) and convert it into text that can be searched, copied, analyzed, etc. The output can be downloaded as a PDF file for french or english input.")

st.markdown("____________________________________")

languages = {
    'French': 'fra',
    'English': 'eng'
}

with st.sidebar:
    st.title("Image-to-Text Converter For French and English documents")
    textOutput = st.selectbox(
        "Output format",
        ('One text file', 'Text file per page'))
    ocr_box = st.selectbox('Select the document language', list(languages.keys()))
    st.markdown(
        "## Notes:  \n - Once you upload the file, a \"Running\" sign with show at the top right \n - Once it has completed running, a button will appear to download the file")
    
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)
    st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"),unsafe_allow_html=True)

    

pdf_file = st.file_uploader("import your PDF", type="pdf")
if pdf_file:
    path = pdf_file.read()
    # display document
    with st.expander("Display document"):
        displayPDF(path)
    # pdf to text
    if textOutput == 'One text file':
        if ocr_box:
            texts, nbPages = images_to_txt(path, languages[ocr_box])
            totalPages = "total number of pages: "+str(nbPages)
            text_data_f = "\n\n".join(texts)
        else:
            text_data_f, nbPages = convert_pdf_to_txt_file(pdf_file)
            totalPages = "total number of pages: "+str(nbPages)       
        with st.expander('PDF infos'):    
            st.info('file name: '+pdf_file.name[:-4])
            st.info(totalPages)
        with st.expander('Display OCR output'):
            user_input = st.write(text_data_f)
        st.download_button("Download text file", text_data_f,file_name=pdf_file.name[:-4]+'.txt')
    else:
        if ocr_box:
            text_data, nbPages = images_to_txt(path, languages[ocr_box])
            totalPages = "total number of pages: "+str(nbPages)
        else:
            text_data, nbPages = convert_pdf_to_txt_pages(pdf_file)
            totalPages = "total number of pages: "+str(nbPages)

        with st.expander('PDF infos'):    
            st.info('file name: '+pdf_file.name[:-4])
            st.info(totalPages)
        with st.expander('Display OCR output'):
            user_input = st.write(text_data)
        zipPath = save_pages(text_data)
        # download text data   
        with open(zipPath, "rb") as fp:
            btn = st.download_button(
                label="Download zip file",
                data=fp,
                file_name=pdf_file.name[:-4]+".zip",
                mime="application/zip"
            )

    
    
