def main():
  #url = "https://www.normanok.gov/sites/default/files/documents/2023-02/2023-01-31_daily_incident_summary.pdf"
  url = input('Please enter the url to the pdf\n')
  u1 = get_pdf(url)

  con = create_table()
  clear_table(con)
  
  store_data_from_pdf(u1, con)

  status(con)


if __name__ == "__main__":
  main()
