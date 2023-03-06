def main():
  url1 = "https://www.normanok.gov/sites/default/files/documents/2023-02/2023-01-31_daily_incident_summary.pdf"

  u1 = get_pdf(url1)

  con = create_table()
  clear_table(con)
  
  store_data_from_pdf(u1, con)

  print_table(con)
