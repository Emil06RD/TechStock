from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "http://localhost:3000"
USERNAME = "admin"
PASSWORD = "admin123"

SCREENSHOTS_DIR = Path("screenshots")
SCREENSHOTS_DIR.mkdir(exist_ok=True)


def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)
    return driver


def save_shot(driver, name: str):
    driver.save_screenshot(str(SCREENSHOTS_DIR / name))


def open_login(driver):
    driver.get(f"{BASE_URL}/login")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )


def wait_for_any(driver, locators, timeout=10):
    wait = WebDriverWait(driver, timeout)
    last_error = None

    for by, value in locators:
        try:
            return wait.until(EC.presence_of_element_located((by, value)))
        except Exception as exc:
            last_error = exc

    if last_error:
        raise last_error
    raise TimeoutException("No se encontró ningún locator válido.")


def wait_clickable_any(driver, locators, timeout=10):
    wait = WebDriverWait(driver, timeout)
    last_error = None

    for by, value in locators:
        try:
            return wait.until(EC.element_to_be_clickable((by, value)))
        except Exception as exc:
            last_error = exc

    if last_error:
        raise last_error
    raise TimeoutException("No se encontró ningún elemento clickable válido.")


def get_username_input(driver):
    return wait_for_any(
        driver,
        [
            (By.ID, "username"),
            (By.NAME, "username"),
            (By.NAME, "user"),
            (By.CSS_SELECTOR, "input[type='text']"),
        ],
    )


def get_password_input(driver):
    return wait_for_any(
        driver,
        [
            (By.ID, "password"),
            (By.NAME, "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
        ],
    )


def get_login_button(driver):
    return wait_clickable_any(
        driver,
        [
            (By.ID, "loginBtn"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.XPATH, "//button[contains(., 'Iniciar')]"),
            (By.XPATH, "//button[contains(., 'Login')]"),
            (By.XPATH, "//input[@type='submit']"),
        ],
    )


def fill_login(driver, username="", password=""):
    user_input = get_username_input(driver)
    pass_input = get_password_input(driver)

    user_input.clear()
    pass_input.clear()

    user_input.send_keys(username)
    pass_input.send_keys(password)


def submit_login(driver):
    get_login_button(driver).click()


def is_logged_in(driver):
    dashboard_clues = [
        (By.XPATH, "//*[contains(text(),'Dashboard')]"),
        (By.XPATH, "//*[contains(text(),'Bienvenido')]"),
        (By.XPATH, "//*[contains(text(),'Productos')]"),
        (By.XPATH, "//*[contains(text(),'Cerrar Sesión')]"),
        (By.XPATH, "//*[contains(text(),'Cerrar Sesion')]"),
    ]
    try:
        wait_for_any(driver, dashboard_clues, timeout=5)
        return True
    except Exception:
        return False


def has_login_form(driver):
    try:
        get_username_input(driver)
        get_password_input(driver)
        return True
    except Exception:
        return False


@pytest.fixture
def driver():
    driver = setup_driver()
    yield driver
    driver.quit()


def test_TC01_login_valido(driver):
    open_login(driver)
    fill_login(driver, USERNAME, PASSWORD)
    submit_login(driver)

    WebDriverWait(driver, 8).until(
        lambda d: d.current_url != f"{BASE_URL}/login" or is_logged_in(d)
    )
    save_shot(driver, "TC01_login_valido.png")

    assert is_logged_in(driver)


def test_TC02_login_invalido(driver):
    open_login(driver)
    fill_login(driver, USERNAME, "clave_incorrecta")
    submit_login(driver)
    save_shot(driver, "TC02_login_invalido.png")

    assert has_login_form(driver)


def test_TC03_login_campos_vacios(driver):
    open_login(driver)
    fill_login(driver, "", "")
    submit_login(driver)
    save_shot(driver, "TC03_login_campos_vacios.png")

    assert has_login_form(driver)


def test_TC04_login_usuario_vacio(driver):
    open_login(driver)
    fill_login(driver, "", PASSWORD)
    submit_login(driver)
    save_shot(driver, "TC04_login_usuario_vacio.png")

    assert has_login_form(driver)


def test_TC05_login_password_vacio(driver):
    open_login(driver)
    fill_login(driver, USERNAME, "")
    submit_login(driver)
    save_shot(driver, "TC05_login_password_vacio.png")

    assert has_login_form(driver)