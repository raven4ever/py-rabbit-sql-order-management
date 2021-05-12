# Order Management Application

## Purpose

Create a Python application to manage the products stock based on received orders.

## Requirements

The application will read the initial stocks from XML files stored at a given path from the file-system. After the
processing is finished, the XML files will be moved to another file-system path.

The application will receive orders using JSON messages sent to the `ORDERS` queue. After processing the order, it will
post a JSON message to the `ORDERS_RESULT` queue. There are 2 possible order statuses: `ACCEPTED`
and `INSUFFICIENT_STOCK`.

## Configuration

All the required configuration is made by editing the [application.properties](./application.properties) file.

## Prerequisites

- MySql server installed and configured
- RabbitMQ server installed and configured

## Testing

The XML format that will be used is:

```xml
<?xml version="1.0"?>
<Stock>
    <Product>
        <id></id>
        <quantity></quantity>
    </Product>
</Stock>
```

The order received message will have the following format:

```json
{
  "client_name": "Name",
  "product_id": 9999,
  "quantity": 666
}
```

The order response message will have the following format:

````json
{
  "order_id": 7777,
  "order_status": "ACCEPTED"
}
````