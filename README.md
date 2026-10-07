# Sleep Disorder Classification

A frontend-only React and TypeScript app for an educational sleep disorder classification project. It includes a home page, validated sleep assessment form, and prediction results page. No machine-learning model or backend is included.

## Run locally

Install Node.js, clone this repository, then run:

```sh
npm install
npm run dev
```

Open the local address printed in the terminal. To create a production build, run `npm run build`.

## Connect a Python prediction API

Create a `.env.local` file in the project root and set your Python API's base URL:

```env
VITE_API_BASE_URL=http://localhost:8000
```

The assessment sends a `POST` request to `${VITE_API_BASE_URL}/predict`. The response must contain a prediction and a confidence value between `0` and `1`, for example:

```json
{
  "prediction": "Insomnia",
  "confidence": 0.87
}
```

Restart the development server after changing the API address. Predictions are unavailable until a compatible Python API is running and connected.

## Tech stack

- React and TypeScript
- TanStack Start and TanStack Router
- Tailwind CSS
- React Hook Form and Zod
