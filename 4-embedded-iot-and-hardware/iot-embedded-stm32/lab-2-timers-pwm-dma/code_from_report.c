// Code extracted from the lab report (report.pdf)

// ---- fragment 1 ----
#include "stm32f1xx.h"

int main(void) {

    // 1. Увімкнення тактування для порту GPIOA
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN;

    // 2. Налаштування піна PA4 як цифрового виходу (push-pull, 10MHz)
    // Спочатку очищуємо поточні налаштування для MODE та CNF
    GPIOA->CRL &= ~(GPIO_CRL_CNF4 | GPIO_CRL_MODE4);
    // Встановлюємо режим: MODE4 = 01 (Output mode, max speed 10 MHz), CNF4 = 00 (Push-pull)
    GPIOA->CRL |= GPIO_CRL_MODE4_0;

    // 3. Короткочасне увімкнення світлодіода при старті програми
    // Це дозволяє візуально визначити момент запуску МК

// ---- fragment 2 ----
    // 4. Налаштування незалежного сторожового таймера IWDG
    // Потрібний час скидання: 5 * N = 5 * 21 = 105 мс
    // Тактова частота LSI ~ 40 кГц
    // Формула таймауту: T = (Prescaler * Reload_Value) / F_LSI

    // Крок 1: Зняти захист регістрів IWDG_PR та IWDG_RLR
    IWDG->KR = 0x5555;

    // Крок 2: Встановити дільник частоти (prescaler)
    // Обираємо Prescaler = 32 (значення в регістрі PR = 3)

// ---- fragment 3 ----
    // Крок 3: Встановити значення перезавантаження лічильника (Reload_Value)
    // Розрахунок: Reload_Value = (T * F_LSI) / Prescaler
    // Reload_Value = (0.105 с * 40000 Гц) / 32 ? 131
    IWDG->RLR = 131;

    // Крок 4: Перезавантажити лічильник IWDG, щоб застосувалися нові значення
    IWDG->KR = 0xAAAA;

    // Крок 5: Запустити таймер IWDG
    IWDG->KR = 0xCCCC;

    // 5. Нескінченний цикл без скидання watchdog'а
    // Програма залишатиметься тут доти, доки IWDG не викличе апаратне скидання МК
    while (1) {
        // Очікуємо на скидання мікроконтролера
    }
}

// ---- fragment 4 ----
#include <stm32f1xx.h>

#define F_CPU 8000000         // Тактова частота МК - 8 МГц
#define LED_ON_TIME_MS  50    // Час увімкненого стану (50 мс)
#define LED_OFF_TIME_MS 15    // Час вимкненого стану (15 мс)
#define TOTAL_PERIOD_MS (LED_ON_TIME_MS + LED_OFF_TIME_MS) // Загальний період (65 мс)

// Глобальний лічильник мілісекунд
volatile unsigned int ms_counter = 0;

int main(void) {
    // 1. Увімкнення тактування порту GPIOA
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN;

    // 2. Налаштування піна PA4 як вихід push-pull, швидкість 10 МГц

// ---- fragment 5 ----
    // 3. Ініціалізація системного таймера SysTick для генерації переривань щомілісекунду
    SysTick_Config(F_CPU / 1000);

    // 4. Нескінченний цикл
    while (1) {
        // Основний цикл залишаємо порожнім, керування LED відбувається у SysTick
    }

    return 0;
}

// Обробник переривання SysTick (викликається кожну мілісекунду)
void SysTickHandler(void) {
    // Збільшення лічильника мілісекунд
    ms_counter++;

    // Керування світлодіодом:
    // 0 .. (LED_ON_TIME_MS-1) - LED увімкнено
    if (ms_counter < LED_ON_TIME_MS) {

// ---- fragment 6 ----
    }
    // LED_OFF_TIME_MS наступні мілісекунди - LED вимкнено
    else {

// ---- fragment 7 ----
    }

    // Перевірка кінця періоду
    if (ms_counter >= TOTAL_PERIOD_MS) {
        ms_counter = 0; // Скидаємо лічильник для нового циклу
    }
}

// ---- fragment 8 ----
#include "stm32f1xx.h"

#define F_APB1 24000000UL  // Частота шини APB1

// Інтервали в "тіках" по 0.1 мс

// ---- fragment 9 ----
// Кількість світлодіодів
#define LED_COUNT 5
#define LED_START_PIN 11  // Світлодіоди підключені до PA11–PA15

// Обробник переривання таймера TIM2
void TIM2_IRQHandler(void) {

// ---- fragment 10 ----
                           GPIO_BSRR_BR14 | GPIO_BSRR_BR15);

            // Включаємо поточний світлодіод
            if (interval_idx < LED_COUNT) {
                GPIOA->BSRR = (1 << (LED_START_PIN + interval_idx));
            }

            // Скидаємо лічильник
            tick_counter = 0;

            // Переходимо до наступного інтервалу
            interval_idx++;
            if (interval_idx >= LED_COUNT) interval_idx = 0;
        }
    }
}

// Ініціалізація таймера TIM2
void timer_init(void) {

// ---- fragment 11 ----
}

// Ініціалізація GPIO для світлодіодів
void GPIO_Init(void) {
    // Увімкнення тактування GPIOA та AFIO
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN | RCC_APB2ENR_AFIOEN;

    // Вимикаємо JTAG, залишаємо SWD
    AFIO->MAPR |= AFIO_MAPR_SWJ_CFG_JTAGDISABLE;

    // PA11–PA15 як виходи push-pull 10 МГц

// ---- fragment 12 ----
                   GPIO_BSRR_BR14 | GPIO_BSRR_BR15);
}

int main(void) {

// ---- fragment 13 ----
    while(1) {
        // Основний цикл порожній, управління світлодіодами через переривання
    }
}

// ---- fragment 14 ----
#include "stm32f1xx.h"

// Ініціалізація периферії
void Peripherals_Init(void) {
    // Увімкнення тактування для GPIOA та альтернативних функцій
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN | RCC_APB2ENR_AFIOEN;
    // Увімкнення тактування для таймерів TIM2 (генерація PWM) та TIM3 (захоплення)
    RCC->APB1ENR |= RCC_APB1ENR_TIM2EN | RCC_APB1ENR_TIM3EN;

    // Налаштування PA0 як вихід PWM (TIM2_CH1)

// ---- fragment 15 ----
        period = capture - last_capture;    // Обчислення періоду
        last_capture = capture;             // Запам’ятовування поточного значення
    }
}

int main(void) {

// ---- fragment 16 ----
    while(1) {
        // Основний цикл порожній, все працює через переривання
        // Змінна 'period' містить період сигналу в тактах таймера
    }
}
