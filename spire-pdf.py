# CreateTaggedPdf.py
from spire.pdf import PdfDocument, PdfPageSize, PdfMargins, TabOrder
from spire.pdf.common import PdfTrueTypeFont, PdfSolidBrush, PdfRGBColor
from spire.pdf.interchange.taggedpdf import PdfTaggedContent, PdfStandardStructTypes
from spire.pdf.tables import PdfTable
from spire.pdf.graphics import PdfImage
from System.Drawing import Font, Color
from System.Drawing import PointF, RectangleF

def main():
    # Create a PdfDocument object
    doc = PdfDocument()

    # Add a page (A4) with margins
    page = doc.Pages.Add(PdfPageSize.A4, PdfMargins(20))

    # Set tab order to structure
    page.TabOrder = TabOrder.Structure

    # Create tagged content for the document
    tagged_content = PdfTaggedContent(doc)

    # Set language and title
    tagged_content.Language = "en-US"
    tagged_content.Title = "Create Tagged PDF in Python"

    # Set PDF/UA-1 identification
    tagged_content.SetPdfUA1Identification()

    # Create font and brush (Times New Roman, 14pt)
    font = PdfTrueTypeFont(Font("Times New Roman", 14), True)
    brush = PdfSolidBrush(PdfRGBColor(Color.Black))

    # Add a "document" element to the structure tree
    document = tagged_content.StructureTreeRoot.AppendChildElement(PdfStandardStructTypes.Document)

    # Add a "heading" element
    heading1 = document.AppendChildElement(PdfStandardStructTypes.HeadingLevel1)
    heading1.BeginMarkedContent(page)
    heading_text = "What Is a Tagged PDF?"
    # draw text at (0,0)
    page.Canvas.DrawString(heading_text, font, brush, PointF(0.0, 0.0))
    heading1.EndMarkedContent(page)

    # Add a "paragraph" element
    paragraph = document.AppendChildElement(PdfStandardStructTypes.Paragraph)
    paragraph.BeginMarkedContent(page)
    paragraph_text = (
        "Tagged PDF doesn’t seem like a life-changing term. But for some, it is. "
        "For people who are blind or have low vision and use assistive technology "
        "(such as screen readers and connected Braille displays) to access information, "
        "an untagged PDF means they are missing out on information contained in the document "
        "because assistive technology cannot “read” untagged PDFs.  Digital accessibility has "
        "opened up so many avenues to information that were once closed to people with visual "
        "disabilities, but PDFs often get left out of the equation."
    )
    # define rectangle area to draw paragraph (x, y, width, height)
    client_size = page.Canvas.ClientSize
    rect = RectangleF(0.0, 30.0, float(client_size.Width), float(client_size.Height))
    page.Canvas.DrawString(paragraph_text, font, brush, rect)
    paragraph.EndMarkedContent(page)

    # Add a "figure" element (image)
    figure = document.AppendChildElement(PdfStandardStructTypes.Figure)
    figure.BeginMarkedContent(page)
    image = PdfImage.FromFile(r"C:\Users\Administrator\Desktop\pdfua.png")
    page.Canvas.DrawImage(image, PointF(0.0, 150.0))
    figure.EndMarkedContent(page)

    # Add a "table" element
    table_elem = document.AppendChildElement(PdfStandardStructTypes.Table)
    table_elem.BeginMarkedContent(page)

    pdf_table = PdfTable()
    pdf_table.Style.DefaultStyle.Font = font

    # simple data source
    data = [
        ["Name", "Age", "Sex"],
        ["John", "22", "Male"],
        ["Katty", "25", "Female"]
    ]
    pdf_table.DataSource = data
    pdf_table.Style.ShowHeader = True

    # draw table at (0, 280) with a max width of 300
    pdf_table.Draw(page.Canvas, PointF(0.0, 280.0), 300.0)

    table_elem.EndMarkedContent(page)

    # Save the document
    doc.SaveToFile("output/CreatePDFUA.pdf")
    doc.Close()

if __name__ == "__main__":
    main()
