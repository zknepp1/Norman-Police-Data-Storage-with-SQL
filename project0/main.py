from project0 import get_pdf, create_table, add_to_table, clear_table, store_data_from_pdf, print_table, status
import sys

def main():

  url = sys.argv[-1]

  u1 = get_pdf(url)

  con = create_table()

  clear_table(con)

  store_data_from_pdf(u1, con)

  status(con)


if __name__ == "__main__":
  main()
