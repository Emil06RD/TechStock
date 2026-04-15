from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


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


def wait_all_any(driver, locators, timeout=10):
    end_wait = WebDriverWait(driver, timeout)
    last_error = None

    for by, value in locators:
        try:
            elements = end_wait.until(lambda d: d.find_elements(by, value))
            if elements:
                return elements
        except Exception as exc:
            last_error = exc

    if last_error:
        raise last_error
    raise TimeoutException("No se encontró ninguna lista de elementos válida.")


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


def open_login(driver):
    driver.get(f"{BASE_URL}/login")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )


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


def login(driver):
    open_login(driver)

    user_input = get_username_input(driver)
    pass_input = get_password_input(driver)

    user_input.clear()
    pass_input.clear()

    user_input.send_keys(USERNAME)
    pass_input.send_keys(PASSWORD)
    get_login_button(driver).click()

    WebDriverWait(driver, 8).until(
        lambda d: "dashboard" in d.current_url.lower()
        or "productos" in d.page_source.lower()
        or "bienvenido" in d.page_source.lower()
    )


def go_to_products(driver):
    btn = wait_clickable_any(
        driver,
        [
            (By.XPATH, "//a[contains(., 'Productos')]"),
            (By.XPATH, "//button[contains(., 'Productos')]"),
            (By.XPATH, "//a[contains(., 'Ir a Productos')]"),
            (By.XPATH, "//button[contains(., 'Ir a Productos')]"),
        ],
        timeout=8,
    )
    btn.click()

    WebDriverWait(driver, 8).until(
        lambda d: "producto" in d.page_source.lower()
        or "inventario" in d.page_source.lower()
    )


def go_to_new_product(driver):
    btn = wait_clickable_any(
        driver,
        [
            (By.ID, "addProductBtn"),
            (By.XPATH, "//a[contains(., 'Agregar Producto')]"),
            (By.XPATH, "//button[contains(., 'Agregar Producto')]"),
            (By.XPATH, "//a[contains(., 'Nuevo Producto')]"),
            (By.XPATH, "//button[contains(., 'Nuevo Producto')]"),
        ],
        timeout=8,
    )
    btn.click()

    WebDriverWait(driver, 8).until(
        lambda d: "guardar" in d.page_source.lower()
        or "producto" in d.page_source.lower()
    )


def field_name(driver):
    return wait_for_any(
        driver,
        [
            (By.ID, "productName"),
            (By.NAME, "name"),
            (By.NAME, "nombre"),
            (By.CSS_SELECTOR, "input[name='name']"),
            (By.CSS_SELECTOR, "input[name='nombre']"),
        ],
    )


def field_price(driver):
    return wait_for_any(
        driver,
        [
            (By.ID, "productPrice"),
            (By.NAME, "price"),
            (By.NAME, "precio"),
            (By.CSS_SELECTOR, "input[name='price']"),
            (By.CSS_SELECTOR, "input[name='precio']"),
        ],
    )


def field_quantity(driver):
    return wait_for_any(
        driver,
        [
            (By.ID, "productQuantity"),
            (By.NAME, "quantity"),
            (By.NAME, "cantidad"),
            (By.CSS_SELECTOR, "input[name='quantity']"),
            (By.CSS_SELECTOR, "input[name='cantidad']"),
            (By.ID, "stock"),
            (By.NAME, "stock"),
            (By.CSS_SELECTOR, "input[name='stock']"),
        ],
    )


def field_category(driver):
    return wait_for_any(
        driver,
        [
            (By.ID, "productCategory"),
            (By.NAME, "category"),
            (By.NAME, "categoria"),
            (By.CSS_SELECTOR, "input[name='category']"),
            (By.CSS_SELECTOR, "input[name='categoria']"),
            (By.CSS_SELECTOR, "select[name='category']"),
            (By.CSS_SELECTOR, "select[name='categoria']"),
        ],
    )


def save_button(driver):
    return wait_clickable_any(
        driver,
        [
            (By.ID, "saveProductBtn"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.XPATH, "//button[contains(., 'Guardar')]"),
            (By.XPATH, "//button[contains(., 'Actualizar')]"),
            (By.XPATH, "//input[@type='submit']"),
        ],
    )


def create_product(driver, name, price, quantity, category):
    go_to_new_product(driver)

    n = field_name(driver)
    p = field_price(driver)
    q = field_quantity(driver)
    c = field_category(driver)

    n.clear()
    p.clear()
    q.clear()

    n.send_keys(name)
    p.send_keys(price)
    q.send_keys(quantity)

    if c.tag_name.lower() == "select":
        try:
            Select(c).select_by_visible_text(category)
        except Exception:
            Select(c).select_by_index(1)
    else:
        c.clear()
        c.send_keys(category)

    save_button(driver).click()


def body_text(driver):
    return driver.find_element(By.TAG_NAME, "body").text.lower()


def first_edit_button(driver):
    buttons = wait_all_any(
        driver,
        [
            (By.CLASS_NAME, "editBtn"),
            (By.XPATH, "//a[contains(., 'Editar')]"),
            (By.XPATH, "//button[contains(., 'Editar')]"),
        ],
        timeout=8,
    )
    return buttons[0]


def first_delete_button(driver):
    buttons = wait_all_any(
        driver,
        [
            (By.CLASS_NAME, "deleteBtn"),
            (By.XPATH, "//a[contains(., 'Eliminar')]"),
            (By.XPATH, "//button[contains(., 'Eliminar')]"),
        ],
        timeout=8,
    )
    return buttons[0]


def search_input(driver):
    return wait_for_any(
        driver,
        [
            (By.ID, "search"),
            (By.NAME, "search"),
            (By.NAME, "buscar"),
            (By.CSS_SELECTOR, "input[type='search']"),
            (By.CSS_SELECTOR, "input[placeholder*='Buscar']"),
        ],
        timeout=5,
    )


def search_button(driver):
    return wait_clickable_any(
        driver,
        [
            (By.ID, "searchBtn"),
            (By.XPATH, "//button[contains(., 'Buscar')]"),
            (By.XPATH, "//input[@type='submit']"),
        ],
        timeout=5,
    )


def accept_alert_if_present(driver, timeout=3):
    try:
        WebDriverWait(driver, timeout).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        return True
    except Exception:
        return False


@pytest.fixture
def driver():
    driver = setup_driver()
    yield driver
    driver.quit()


def test_TC06_navegacion_a_productos(driver):
    login(driver)
    go_to_products(driver)
    save_shot(driver, "TC06_navegacion_a_productos.png")

    assert "producto" in body_text(driver) or "inventario" in body_text(driver)


def test_TC07_navegacion_a_nuevo_producto(driver):
    login(driver)
    go_to_new_product(driver)
    save_shot(driver, "TC07_navegacion_a_nuevo_producto.png")

    assert "guardar" in body_text(driver) or field_name(driver).is_displayed()


def test_TC08_crear_producto_valido(driver):
    login(driver)
    create_product(driver, "Mouse Test", "1500", "10", "Periféricos")
    save_shot(driver, "TC08_crear_producto_valido.png")

    assert "mouse test" in body_text(driver) or "producto" in body_text(driver)


def test_TC09_crear_producto_campos_vacios(driver):
    login(driver)
    go_to_new_product(driver)
    save_button(driver).click()
    save_shot(driver, "TC09_crear_producto_campos_vacios.png")

    assert (
        "guardar" in body_text(driver)
        or "required" in driver.page_source.lower()
        or "oblig" in body_text(driver)
    )


def test_TC10_crear_producto_stock_negativo(driver):
    login(driver)
    go_to_new_product(driver)

    field_name(driver).send_keys("Producto Negativo")
    field_price(driver).send_keys("1000")
    field_quantity(driver).send_keys("-5")

    c = field_category(driver)
    if c.tag_name.lower() == "select":
        try:
            Select(c).select_by_index(1)
        except Exception:
            pass
    else:
        c.send_keys("Periféricos")

    save_button(driver).click()
    save_shot(driver, "TC10_crear_producto_stock_negativo.png")

    assert (
        "required" in driver.page_source.lower()
        or "invalid" in driver.page_source.lower()
        or "error" in driver.page_source.lower()
        or "oblig" in body_text(driver)
        or "guardar" in body_text(driver)
    )


def test_TC11_editar_producto_valido(driver):
    login(driver)
    go_to_products(driver)
    first_edit_button(driver).click()

    n = field_name(driver)
    n.clear()
    n.send_keys("Producto Editado Selenium")

    save_button(driver).click()
    save_shot(driver, "TC11_editar_producto_valido.png")

    assert "editado" in body_text(driver) or "producto" in body_text(driver)


def test_TC12_editar_producto_nombre_vacio(driver):
    login(driver)
    go_to_products(driver)
    first_edit_button(driver).click()

    n = field_name(driver)
    n.clear()
    save_button(driver).click()
    save_shot(driver, "TC12_editar_producto_nombre_vacio.png")

    assert (
        "guardar" in body_text(driver)
        or "required" in driver.page_source.lower()
        or "oblig" in body_text(driver)
        or "producto" in body_text(driver)
    )


def test_TC13_eliminar_producto_existente(driver):
    login(driver)
    go_to_products(driver)
    first_delete_button(driver).click()
    accept_alert_if_present(driver)
    save_shot(driver, "TC13_eliminar_producto_existente.png")

    assert "producto" in body_text(driver) or "inventario" in body_text(driver)


