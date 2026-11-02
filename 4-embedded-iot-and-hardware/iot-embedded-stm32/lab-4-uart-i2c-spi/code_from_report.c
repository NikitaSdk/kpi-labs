// Code extracted from the lab report (report.pdf)

// ---- fragment 1 ----
#include "stm32f1xx.h"

/*
 * Обробник переривання USART1.
 * Викликається при надходженні байта даних по інтерфейсу UART.
 */
void USART1_IRQHandler(void)
{
    /* Перевірка прапора прийому даних */
    if (USART1->SR & USART_SR_RXNE)
    {
        /* Зчитування прийнятого символу */
        uint8_t received_char = USART1->DR;

        /* Обробка даних: збільшення значення на 1 */
        uint8_t next_val = ((received_char - '0') + 1) % 10;

        /* Очікування готовності передавача */
        while (!(USART1->SR & USART_SR_TXE));

        /* Передача обробленого символу у зворотному напрямку */
        USART1->DR = next_val + '0';
    }
}

int main(void)
{
    /* Увімкнення тактування порту GPIOA, модуля AFIO та USART1 */
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN |
        RCC_APB2ENR_AFIOEN |
        RCC_APB2ENR_USART1EN;

    /* Налаштування PA9 як TX USART1 (альтернативна функція, Push-Pull) */
    GPIOA->CRH &= ~GPIO_CRH_CNF9;
    GPIOA->CRH |= GPIO_CRH_CNF9_1;
    GPIOA->CRH |= GPIO_CRH_MODE9;

    /* Налаштування PA10 як RX USART1 (вхід з плаваючим рівнем) */
    GPIOA->CRH &= ~GPIO_CRH_CNF10;
    GPIOA->CRH |= GPIO_CRH_CNF10_0;
    GPIOA->CRH &= ~GPIO_CRH_MODE10;

    /* Налаштування USART1: швидкість 9600 бод при частоті 8 МГц */
    USART1->BRR = 0x341;

    /* Формат кадру: 8 біт даних, без перевірки парності */
    USART1->CR1 &= ~USART_CR1_M;
    USART1->CR1 &= ~USART_CR1_PCE;

    /* Один стоп-біт */
    USART1->CR2 &= ~USART_CR2_STOP;

    /* Увімкнення приймача, передавача, переривання RX та самого USART */
    USART1->CR1 |= USART_CR1_RE |
        USART_CR1_TE |
        USART_CR1_RXNEIE |
        USART_CR1_UE;

    /* Дозвіл переривань USART1 у NVIC */
    NVIC_EnableIRQ(USART1_IRQn);
    __enable_irq();

    /* Передача початкового символу для запуску обміну */
    while (!(USART1->SR & USART_SR_TXE));
    USART1->DR = '0';

    /* Основний цикл програми */
    while (1)
    {
        /* Обмін даними виконується виключно у перериваннях */
    }
}

// ---- fragment 2 ----
#include "stm32f1xx.h"

/*
 * Обробник переривання USART1.
 * Викликається при прийомі символу від іншого мікроконтролера.
 */
void USART1_IRQHandler(void)
{
    if (USART1->SR & USART_SR_RXNE)
    {
        /* Зчитування прийнятого символу */
        uint8_t received_char = USART1->DR;

        /* Обробка даних: збільшення значення на 1 */
        uint8_t next_val = ((received_char - '0') + 1) % 10;

        /* Очікування готовності передавача */
        while (!(USART1->SR & USART_SR_TXE));

        /* Передача відповіді */
        USART1->DR = next_val + '0';
    }
}

int main(void)
{
    /* Увімкнення тактування GPIOA, AFIO та USART1 */
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN |
        RCC_APB2ENR_AFIOEN |
        RCC_APB2ENR_USART1EN;

    /* PA9 – TX USART1 */
    GPIOA->CRH &= ~GPIO_CRH_CNF9;
    GPIOA->CRH |= GPIO_CRH_CNF9_1;
    GPIOA->CRH |= GPIO_CRH_MODE9;

    /* PA10 – RX USART1 */
    GPIOA->CRH &= ~GPIO_CRH_CNF10;
    GPIOA->CRH |= GPIO_CRH_CNF10_0;
    GPIOA->CRH &= ~GPIO_CRH_MODE10;

    /* Швидкість обміну 9600 бод */
    USART1->BRR = 0x341;

    /* 8 біт даних, без перевірки парності */
    USART1->CR1 &= ~USART_CR1_M;
    USART1->CR1 &= ~USART_CR1_PCE;

    /* Один стоп-біт */
    USART1->CR2 &= ~USART_CR2_STOP;

    /* Увімкнення USART, RX, TX та переривань */
    USART1->CR1 |= USART_CR1_RE |
        USART_CR1_TE |
        USART_CR1_RXNEIE |
        USART_CR1_UE;

    /* Дозвіл переривань USART1 */
    NVIC_EnableIRQ(USART1_IRQn);
    __enable_irq();

    /* Основний цикл */
    while (1)
    {
        /* Взаємодія відбувається у перериваннях */
    }
}

// ---- fragment 3 ----
#include "stm32f1xx.h"
/*
 * Обробник переривання USART1.
 * Забезпечує прийом та передачу даних у одноранговому режимі.
 */
void USART1_IRQHandler(void)
{
    if (USART1->SR & USART_SR_RXNE)
    {
        /* Зчитування прийнятого символу */
        uint8_t received_char = USART1->DR;

        /* Обробка даних: збільшення значення на 1 */
        uint8_t next_val = ((received_char - '0') + 1) % 10;

        /* Очікування готовності передавача */
        while (!(USART1->SR & USART_SR_TXE));

        /* Передача результату обробки */
        USART1->DR = next_val + '0';
    }
}

int main(void)
{
    /* Увімкнення тактування GPIOA, AFIO та USART1 */
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN |
        RCC_APB2ENR_AFIOEN |
        RCC_APB2ENR_USART1EN;

    /* Налаштування PA9 як TX USART1 */
    GPIOA->CRH &= ~GPIO_CRH_CNF9;
    GPIOA->CRH |= GPIO_CRH_CNF9_1;
    GPIOA->CRH |= GPIO_CRH_MODE9;

    /* Налаштування PA10 як RX USART1 */
    GPIOA->CRH &= ~GPIO_CRH_CNF10;
    GPIOA->CRH |= GPIO_CRH_CNF10_0;
    GPIOA->CRH &= ~GPIO_CRH_MODE10;

    /* Налаштування швидкості обміну 9600 бод */
    USART1->BRR = 0x341;

    /* Формат кадру: 8 біт, без парності */
    USART1->CR1 &= ~USART_CR1_M;
    USART1->CR1 &= ~USART_CR1_PCE;

    /* Один стоп-біт */
    USART1->CR2 &= ~USART_CR2_STOP;

    /* Увімкнення USART та переривань */
    USART1->CR1 |= USART_CR1_RE |
        USART_CR1_TE |
        USART_CR1_RXNEIE |
        USART_CR1_UE;

    /* Дозвіл переривань USART1 */
    NVIC_EnableIRQ(USART1_IRQn);
    __enable_irq();

    /* Основний цикл програми */
    while (1)
    {
        /* Логіка обміну реалізована в обробнику переривань */
    }
}
