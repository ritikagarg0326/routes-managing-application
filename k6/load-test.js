import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
    vus: 10,
    duration: "30s",
};

const BASE_URL = "http://localhost:5000";

export default function () {

    // =====================================================
    // 1. HEALTH CHECK
    // =====================================================

    let response = http.get(`${BASE_URL}/api/health`);

    check(response, {
        "health - 200": (r) => r.status === 200,
    });


    // =====================================================
    // 2. GET STATISTICS
    // =====================================================

    response = http.get(`${BASE_URL}/api/stats`);

    check(response, {
        "stats - 200": (r) => r.status === 200,
    });


    // =====================================================
    // 3. SUPPLIERS
    // =====================================================

    response = http.get(`${BASE_URL}/suppliers`);

    check(response, {
        "suppliers GET - 200": (r) => r.status === 200,
    });

    const supplierData = {
        name: `k6-test-supplier-${__VU}-${__ITER}`,
        manager: `k6-user-${__VU}`,
        phone: `99999${String(__VU).padStart(5, "0")}`,
        status: "Active",
    };

    response = http.post(
        `${BASE_URL}/suppliers`,
        supplierData
    );

    check(response, {
        "supplier POST - successful": (r) =>
            r.status >= 200 && r.status < 400,
    });


    // =====================================================
    // 4. TRUCKS
    // =====================================================

    response = http.get(`${BASE_URL}/trucks`);

    check(response, {
        "trucks GET - 200": (r) => r.status === 200,
    });

    const truckData = {
        registration: `K6-TRUCK-${__VU}-${__ITER}`,
        driver: `K6 Driver ${__VU}`,
        capacity: "20",
        status: "Available",
    };

    response = http.post(
        `${BASE_URL}/trucks`,
        truckData
    );

    check(response, {
        "truck POST - successful": (r) =>
            r.status >= 200 && r.status < 400,
    });


    // =====================================================
    // 5. PRODUCTS
    // =====================================================

    response = http.get(`${BASE_URL}/products`);

    check(response, {
        "products GET - 200": (r) => r.status === 200,
    });

    const productData = {
        name: `K6 Test Product ${__VU}-${__ITER}`,
        sku: `K6-SKU-${__VU}-${__ITER}`,
        quantity: "100",
    };

    response = http.post(
        `${BASE_URL}/products`,
        productData
    );

    check(response, {
        "product POST - successful": (r) =>
            r.status >= 200 && r.status < 400,
    });


    // =====================================================
    // 6. ROUTES
    // =====================================================

    response = http.get(`${BASE_URL}/routes`);

    check(response, {
        "routes GET - 200": (r) => r.status === 200,
    });

    const routeData = {
        origin: `K6 Warehouse ${__VU}`,
        destination: `K6 Destination ${__ITER}`,
        distance_km: "250",
    };

    response = http.post(
        `${BASE_URL}/routes`,
        routeData
    );

    check(response, {
        "route POST - successful": (r) =>
            r.status >= 200 && r.status < 400,
    });


    // =====================================================
    // 7. TICKETS
    // =====================================================

    response = http.get(`${BASE_URL}/tickets`);

    check(response, {
        "tickets GET - 200": (r) => r.status === 200,
    });

    const ticketData = {
        title: `K6 Test Ticket ${__VU}-${__ITER}`,
        description: `Load testing ticket created by k6 VU ${__VU}`,
        priority: "Medium",
        status: "Open",
        assignee: `k6-user-${__VU}`,
        jira_key: `K6-${__VU}-${__ITER}`,
    };

    response = http.post(
        `${BASE_URL}/tickets`,
        ticketData
    );

    check(response, {
        "ticket POST - successful": (r) =>
            r.status >= 200 && r.status < 400,
    });


    // =====================================================
    // 8. WAIT BEFORE NEXT ITERATION
    // =====================================================

    sleep(1);
}