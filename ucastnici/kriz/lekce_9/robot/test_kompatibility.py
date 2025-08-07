#před použitím instaluj pip install setuptools
import pkg_resources

def check_versions():
    try:
        selenium_version = pkg_resources.get_distribution("selenium").version
        rfsl_version = pkg_resources.get_distribution("robotframework-seleniumlibrary").version
    except pkg_resources.DistributionNotFound as e:
        print(f"Není nainstalován balíček: {e}")
        return

    print(f"Selenium verze: {selenium_version}")
    print(f"Robotframework-SeleniumLibrary verze: {rfsl_version}")

    # Kontrola kompatibility (jednoduché pravidlo)
    selenium_major = int(selenium_version.split('.')[0])
    rfsl_major = int(rfsl_version.split('.')[0])

    if selenium_major >= 4 and rfsl_major < 6:
        print("⚠️ Varování: Máš novou verzi Selenium (4.x), ale starou SeleniumLibrary (<6), která nemusí být kompatibilní!")
        print("Doporučuji spustit:\n    pip install --upgrade robotframework-seleniumlibrary")
    else:
        print("Verze vypadají kompatibilní. 👍")

if __name__ == "__main__":
    check_versions()
