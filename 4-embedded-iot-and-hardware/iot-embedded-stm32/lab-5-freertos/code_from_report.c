// Code extracted from the lab report (report.pdf)

// ---- fragment 1 ----
void vPeriodicTask300ms(void* pvParameters)
{
    (void)pvParameters;

    for (;;)
    {
        vTaskSuspendAll();
        printf("Periodic task executed every 300 ms\r\n");
        xTaskResumeAll();
        vTaskDelay(pdMS_TO_TICKS(300));
    }
}

int main(void)
{
    xTaskCreate(
        vPeriodicTask300ms,
        "Periodic300",
        1000,
        NULL,
        tskIDLE_PRIORITY + 1,
        NULL
    );

    vTaskStartScheduler();

    for (;;);
}

// ---- fragment 2 ----
void vHighPriorityTask(void* pvParameters)
{
    (void)pvParameters;

    for (;;)
    {
        vTaskSuspendAll();
        printf("Task 1 (High Priority) is running\r\n");
        xTaskResumeAll();

        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

void vLowPriorityTask(void* pvParameters)
{
    (void)pvParameters;

    for (;;)
    {
        vTaskSuspendAll();
        printf("Task 2 (Low Priority) is running\r\n");
        xTaskResumeAll();

        vTaskDelay(pdMS_TO_TICKS(750));
    }
}

int main(void)
{
    xTaskCreate(
        vHighPriorityTask,
        "HighTask",
        1000,
        NULL,
        3,          // високий пріоритет
        NULL
    );

    xTaskCreate(
        vLowPriorityTask,
        "LowTask",
        1000,
        NULL,
        1,          // низький пріоритет
        NULL
    );

    vTaskStartScheduler();

    for (;;);
}

// ---- fragment 3 ----
QueueHandle_t xQueue;

static void vWriterTask(void* pvParameters)
{
    int valueToSend = (int)pvParameters;
    const TickType_t xDelay = pdMS_TO_TICKS(2000);

    for (;;)
    {
        vTaskSuspendAll();
        printf("Writer task sending: %d\r\n", valueToSend);
        xTaskResumeAll();

        if (xQueueSend(xQueue, &valueToSend, 0) != pdPASS)
        {
            vTaskSuspendAll();
            printf("Writer with value %d: Queue is full, WAITING...\r\n", valueToSend);
            xTaskResumeAll();

            xQueueSend(xQueue, &valueToSend, portMAX_DELAY);
        }

        vTaskDelay(xDelay);
    }
}

static void vReaderTask(void* pvParameters)
{
    int receivedValue;
    const TickType_t xReaderDelay = pdMS_TO_TICKS(500);

    for (;;)
    {
        xQueueReceive(xQueue, &receivedValue, portMAX_DELAY);

        vTaskSuspendAll();
        printf("Reader task received: %d\r\n", receivedValue);
        xTaskResumeAll();

        vTaskDelay(xReaderDelay);
    }
}

int main(void)
{
    prvSetupHardware();

    xQueue = xQueueCreate(4, sizeof(int));

    if (xQueue != NULL)
    {
        xTaskCreate(
            vWriterTask,
            "Writer 1 (min)",
            configMINIMAL_STACK_SIZE,
            (void*)1,
            tskIDLE_PRIORITY + 1,
            NULL
        );

        xTaskCreate(
            vWriterTask,
            "Writer 2 (avg)",
            configMINIMAL_STACK_SIZE,
            (void*)5,
            tskIDLE_PRIORITY + 2,
            NULL
        );

        xTaskCreate(
            vWriterTask,
            "Writer 3 (max)",
            configMINIMAL_STACK_SIZE,
            (void*)10,
            tskIDLE_PRIORITY + 3,
            NULL
        );

        xTaskCreate(
            vReaderTask,
            "Reader",
            configMINIMAL_STACK_SIZE,
            NULL,
            tskIDLE_PRIORITY + 4,
            NULL
        );

        vTaskStartScheduler();
    }

    for (;;);
}

static void prvSetupHardware(void)
{
}

// ---- fragment 4 ----
static const char* pcMessagesToSend[] =
{
    "Message from Sender 1 *\r\n",
    "Message from Sender 2 -\r\n"
};

QueueHandle_t xPrintQueue;

int main(void)
{
    prvSetupHardware();

    xPrintQueue = xQueueCreate(5, sizeof(char*));

    if (xPrintQueue != NULL)
    {
        xTaskCreate(
            vSenderTask,
            "Sender 1",
            configMINIMAL_STACK_SIZE,
            (void*)pcMessagesToSend[0],
            tskIDLE_PRIORITY + 1,
            NULL
        );

        xTaskCreate(
            vSenderTask,
            "Sender 2",
            configMINIMAL_STACK_SIZE,
            (void*)pcMessagesToSend[1],
            tskIDLE_PRIORITY + 1,
            NULL
        );

        xTaskCreate(
            vGatekeeperTask,
            "Gatekeeper",
            configMINIMAL_STACK_SIZE,
            NULL,
            tskIDLE_PRIORITY,
            NULL
        );

        vTaskStartScheduler();
    }

    for (;;);
    return 0;
}

static void vSenderTask(void* pvParameters)
{
    char* pcMessageToSend;
    TickType_t xDelayTime;

    pcMessageToSend = (char*)pvParameters;

    if (pcMessageToSend == pcMessagesToSend[0])
    {
        xDelayTime = pdMS_TO_TICKS(1000);
    }
    else
    {
        xDelayTime = pdMS_TO_TICKS(1500);
    }

    for (;;)
    {
        xQueueSend(xPrintQueue, &pcMessageToSend, portMAX_DELAY);
        vTaskDelay(xDelayTime);
    }
}

static void vGatekeeperTask(void* pvParameters)
{
    char* pcReceivedMessage;

    for (;;)
    {
        xQueueReceive(xPrintQueue, &pcReceivedMessage, portMAX_DELAY);
        printf("%s", pcReceivedMessage);
        fflush(stdout);
    }
}

static void prvSetupHardware(void)
{
}
