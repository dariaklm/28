import pytest


from pages.auth_page import AuthPage
from pages.config_page import RegPage


# Тест-кейс EXP-001
# Корректное отображение "Стандартной страницы авторизации"
def test_start_page_is_correct(web_browser):
    page = AuthPage(web_browser)
    phone_tab_class = page.phone_tab.get_attribute("class")
    assert phone_tab_class == "rt-tab rt-tab--small rt-tab--active"
    assert page.phone.is_clickable()
    assert page.password.is_clickable()
    assert page.btn_login.is_clickable()
    assert page.registration_link.is_clickable()
    assert page.auth_title.get_text() == "Авторизация"
    assert page.logo_lk.get_text() == "Личный кабинет"


# Тест-кейс EXP-002 (Bugs-BR-001)
# Проверка элементов в левом и правом блоке страницы
@pytest.mark.xfail(reason="Расположение элементов на странице не соответсвует ТЗ")
def test_location_of_page_blocks(web_browser):
    page = AuthPage(web_browser)
    assert page.auth_form.find(timeout=1)
    assert page.lk_form.find(timeout=1)


# Тест-кейс EXP-003(Bugs-BR-002)
# Проверка названия вкладки "Номер"
@pytest.mark.xfail(reason="Название вкладки 'Номер' не соответствует ТЗ")
def test_phone_tab(web_browser):
    page = AuthPage(web_browser)
    assert page.phone_tab.get_text() == "Номер"


# Тест-кейс EXP-004(Bugs-BR-003)
# Проверка названия кнопки "Продолжить" в форме "Регистрация"
@pytest.mark.xfail(reason="Кнопка должна иметь текст 'Продолжить'")
def test_registration_page_and_continue_button(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    assert reg_page.name_field_text.get_text() == "Имя"
    assert reg_page.last_name_field_text.get_text() == "Фамилия"
    assert reg_page.region_field_text.get_text() == "Регион"
    assert reg_page.email_or_mobile_phone_field_text.get_text() == "E-mail или мобильный телефон"
    assert reg_page.password_field_text.get_text() == "Пароль"
    assert reg_page.password_confirmation_field_text.get_text() == "Подтверждение пароля"
    assert reg_page.continue_button.get_text() == "Продолжить"


# Тест-кейс EXP-005
# Регистрация пользователя с пустым полем "Имя", появления текста с подсказкой об ошибке
def test_registration_page_with_empty_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('')
    reg_page.last_name_field.send_keys("Королькова")
    reg_page.email_or_mobile_phone_field.send_keys("elya_93_93@inbox.ru")
    reg_page.password_field.send_keys("Qwerty12345*")
    reg_page.password_confirmation_field.send_keys("Qwerty12345*")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс EXP-006
# Регистрация пользователя со значением в поле "Имя" меньше 2 символов, появление текста с подсказкой об ошибке
def test_registration_with_an_incorrect_value_in_the_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys('Э')
    reg_page.last_name_field.send_keys("Королькова")
    reg_page.email_or_mobile_phone_field.send_keys("elya_93_93@inbox.ru")
    reg_page.password_field.send_keys("Qwerty12345*")
    reg_page.password_confirmation_field.send_keys("Qwerty12345*")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс EXP-007
# Регистрация пользователя со значением в поле "Фамилия" превышающим 30 символов), появление текста с подсказкой об ошибке
def test_registration_with_an_incorrect_value_in_the_last_name_field(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Маша")
    reg_page.last_name_field.send_keys("аппроолдджэфыввааппрпородддд")
    reg_page.email_or_mobile_phone_field.send_keys("masha_123@mail.ru")
    reg_page.password_field.send_keys("Qwerty123*")
    reg_page.password_confirmation_field.send_keys("Qwerty123*")
    reg_page.continue_button.click()
    reg_page.error_message_name.is_visible()
    assert reg_page.error_message_last_name.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс EXP-008
# Регистрация пользователя с уже зарегистрированным номером, появление оповещения
def test_registration_of_an_already_registered_user(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Эля")
    reg_page.last_name_field.send_keys("Корольковаа")
    reg_page.email_or_mobile_phone_field.send_keys("+79222085264")
    reg_page.password_field.send_keys("142536-Hn")
    reg_page.password_confirmation_field.send_keys("142536-Hn")
    reg_page.continue_button.click()
    assert reg_page.notification_form.is_visible


# Тест-кейс EXP-009(Bugs-BR-004)
# Проверка значка "х" - закрыть всплывающее окно оповещения
@pytest.mark.xfail(reason="Должен быть значок закрыть 'х'")
def test_notification_form(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Эля")
    reg_page.last_name_field.send_keys("Королькова")
    reg_page.email_or_mobile_phone_field.send_keys("+79222085264")
    reg_page.password_field.send_keys("Qwerty12345*")
    reg_page.password_confirmation_field.send_keys("Qwerty12345*")
    reg_page.continue_button.click()
    assert reg_page.login_button.get_text() == 'Войти'
    assert reg_page.recover_password_button.get_text() == 'Восстановить пароль'
    assert reg_page.close_button.get_text() == 'x'


# Тест-кейс EXP-010
#  При регистрации пользователя введен пароль содержащий менее 8 символов, появление текста с подсказкой об ошибке
def test_incorrect_password_during_registration(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Александр")
    reg_page.last_name_field.send_keys("Воропаев")
    reg_page.email_or_mobile_phone_field.send_keys("apokalipsis15@inbox.ru")
    reg_page.password_field.send_keys("Asd123")
    reg_page.password_confirmation_field.send_keys("Asd123")
    reg_page.continue_button.click()
    assert reg_page.error_message_password.get_text() == "Длина пароля должна быть не менее 8 символов"


# Тест-кейс EXP-011
# При регистрация пользователя в поле "Фамилия" введено значение, содержащее недопустимые символы вместо кириллицы
def test_instead_of_cyrillic_invalid_characters(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Эля")
    reg_page.last_name_field.send_keys("***%%%")
    reg_page.email_or_mobile_phone_field.send_keys("elya_93_93@inbox.ru")
    reg_page.password_field.send_keys("Qwerty12345*")
    reg_page.password_confirmation_field.send_keys("Qwerty12345*")
    reg_page.continue_button.click()
    assert reg_page.message_must_be_filled_in_cyrillic.get_text() == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."


# Тест-кейс EXP-012
# Значения в поле ввода "Пароль" и поле ввода "Подтверждение пароля" в форме "Регистрация" не совпадают
def test_password_and_password_confirmation_do_not_match(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Эля")
    reg_page.last_name_field.send_keys("Королькова")
    reg_page.email_or_mobile_phone_field.send_keys("elya_93_93@inbox.ru")
    reg_page.password_field.send_keys("Qwerty12345*")
    reg_page.password_confirmation_field.send_keys("Qwerty12345+")
    reg_page.continue_button.click()
    assert reg_page.message_passwords_dont_match.get_text() == "Пароли не совпадают"


# Тест-кейс EXP-013
# Не валидный email в поле ввода "Email или мобильный телефон" в форме регистрация
def test_invalid_email_or_mobile_phone(web_browser):
    auth_page = AuthPage(web_browser)
    auth_page.registration_link.click()
    reg_page = RegPage(web_browser, auth_page.get_current_url())
    reg_page.name_field.send_keys("Эля")
    reg_page.last_name_field.send_keys("Королькова")
    reg_page.email_or_mobile_phone_field.send_keys("elya_93_93inbox.ru")
    reg_page.password_field.send_keys("Qwerty12345*")
    reg_page.password_confirmation_field.send_keys("Qwerty12345*")
    reg_page.continue_button.click()
    assert reg_page.message_enter_the_phone_in_the_format.get_text() == "Введите телефон в формате +7ХХХХХХХХХХ или" \
                                                                        " +375XXXXXXXXX, или email в формате example@email.ru"


# Тест-кейс EXP-014
# Вход по неправильному паролю в форме "Авторизация" уже зарегистрированного пользователя, надпись "Забыл пароль"
# перекрашивается в оранжевый цвет
def test_authorization_of_a_user_with_an_invalid_password(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys('+79222085164')
    page.password.send_keys("Test")
    page.btn_login.click()
    assert page.message_invalid_username_or_password.get_text() == "Неверный логин или пароль"
    assert "rt-link--orange" in page.the_element_forgot_the_password.get_attribute('class')


# Тест-кейс EXP-015
# Тестирование аутентификации зарегестрированного пользователя
def test_authorisation_valid(web_browser):
    page = AuthPage(web_browser)
    page.phone.send_keys("+79222085164")
    page.password.send_keys("142536-Hn")
    page.btn_login.click()

    assert 'https://b2c.passport.rt.ru/account_b2c/page?state=' in page.get_current_url() \
           and '&client_id=account_b2c#/' in page.get_current_url()