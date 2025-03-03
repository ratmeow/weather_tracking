document.addEventListener("DOMContentLoaded", () => {
  console.log("Скрипт загружен и работает");
  const form = document.querySelector("form");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    // Удаляем предыдущие сообщения об ошибках, если они есть
    removeErrorMessage();

    // Получаем значения полей формы
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");
    const repeatPasswordInput = document.getElementById("repeat-password");

    const username = usernameInput.value.trim();
    const password = passwordInput.value;
    const repeatPassword = repeatPasswordInput.value;

    // Проверяем, совпадают ли пароли
    if (password !== repeatPassword) {
      displayError("Passwords don't match.");
      // Можно добавить класс ошибки для поля повторного ввода
      repeatPasswordInput.classList.add("is-invalid");
      return;
    }

    // Формируем объект с данными для отправки
    const payload = {
      login: username,
      password: password,
    };

    try {
      const response = await fetch("/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        // Если регистрация прошла успешно, перенаправляем пользователя
        const redirectUrl = "/login";
        window.location.href = redirectUrl;
      } else {
        // Если сервер вернул ошибку, выводим сообщение
        const errorData = await response.json();
        displayError(errorData.detail || "Registration failed.");
        // При необходимости можно добавить отметку об ошибке для конкретных полей
      }
    } catch (error) {
      displayError("An error occurred. Please try again later.");
    }
  });
});

/**
 * Функция для отображения сообщения об ошибке.
 * Создает (или обновляет) элемент alert над формой.
 */
function displayError(message) {
  let errorContainer = document.getElementById("error-container");
  if (!errorContainer) {
    errorContainer = document.createElement("div");
    errorContainer.id = "error-container";
    errorContainer.className = "alert alert-danger";
    // Вставляем контейнер с ошибкой перед формой (или в нужное место по дизайну)
    const formContainer = document.querySelector(".row.justify-content-center");
    formContainer.parentNode.insertBefore(errorContainer, formContainer);
  }
  errorContainer.textContent = message;
}

/**
 * Функция для удаления ранее отображенного сообщения об ошибке.
 */
function removeErrorMessage() {
  const errorContainer = document.getElementById("error-container");
  if (errorContainer) {
    errorContainer.remove();
  }
}
