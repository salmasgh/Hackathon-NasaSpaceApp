# NASA Data Fetching API

## Overview

This API allows users to fetch data from NASA's database by providing a bounding box defined by four mandatory coordinates. It retrieves various datasets related to soil moisture, albedo, vegetation water content, and other relevant environmental information.

## Features

- Fetches data from NASA's database based on a specified bounding box.
- Requires four mandatory coordinates to define the area of interest.
- Returns data in a structured JSON format for easy consumption by client applications.

## API Endpoint

### Fetch Data

### Query Parameters

The API requires the following query parameters:

- `bounding_box`: The coordinates that define the bounding box.
  - **Format**: `bounding_box=lowerLeftLon,lowerLeftLat,upperRightLon,upperRightLat`
  - **Example**: `bounding_box=-120.0,35.0,-100.0,50.0`

### Example Request

```http
GET http://localhost:5000/api/data?bounding_box=-120.0,35.0,-100.0,50.0


