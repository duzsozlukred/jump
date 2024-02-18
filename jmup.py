import subprocess
import re

def get_ip(website):
  """
  Web sitesinin IP adresini döndürür.

  Args:
    website: Web sitesinin URL'si.

  Returns:
    Web sitesinin IP adresi.
  """
  command = ["ping", "-c", "1", website]
  process = subprocess.Popen(command, stdout=subprocess.PIPE)
  output, _ = process.communicate()
  match = re.search(r"PING (\d+\.\d+\.\d+\.\d+)", output.decode("utf-8"))
  if match:
    return match.group(1)
  else:
    return None

def get_subdomains(ip):
  """
  Bir IP adresinin tüm alt alanlarını döndürür.

  Args:
    ip: IP adresi.

  Returns:
    Alt alanların listesi.
  """
  command = ["dig", "+short", "-x", ip]
  process = subprocess.Popen(command, stdout=subprocess.PIPE)
  output, _ = process.communicate()
  subdomains = output.decode("utf-8").splitlines()
  return subdomains

def check_takeover(subdomain):
  """
  Bir alt alan adında takeover açığı olup olmadığını kontrol eder.

  Args:
    subdomain: Alt alan adı.

  Returns:
    Takeover açığı varsa True, yoksa False.
  """
  command = ["curl", "-s", "-I", subdomain]
  process = subprocess.Popen(command, stdout=subprocess.PIPE)
  output, _ = process.communicate()
  headers = output.decode("utf-8").splitlines()
  for header in headers:
    if "Server:" in header and "GitHub" in header:
      return True
  return False

def main():
  """
  Kullanıcıdan web sitesini ister ve tüm alt alanlarını bulur ve takeover açığı olanları yazdırır.
  """
  website = input("Web sitesini girin: ")
  ip = get_ip(website)
  if ip is None:
    print(f"{website} için IP adresi bulunamadı.")
    return
  print(f"{website} için IP adresi: {ip}")
  subdomains = get_subdomains(ip)
  print(f"{website} için alt alanlar:")
  for subdomain in subdomains:
    print(f"- {subdomain}")
  print("Takeover açığı olan alt alanlar:")
  for subdomain in subdomains:
    if check_takeover(subdomain):
      print(f"- {subdomain}")

if __name__ == "__main__":
  main()
