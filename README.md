# Coach Platform

A streamlined coaching platform for fitness professionals to manage exercise libraries, client assessments, and generate AI-powered workout plans.

## Features

- **Exercise Library**: Create and organize exercises with AI-augmented tagging
- **Client Management**: Track client profiles and assessment history
- **Comprehensive Assessments**: FMS scoring, body metrics, health history, lifestyle factors
- **AI-Powered Plan Generation**: Generate personalized 4-week workout plans (using Claude 4.5)
- **Email Delivery**: Send workout plans directly to clients

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS |
| Backend | Python FastAPI |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth |
| AI | Anthropic Claude 4.5 |
| Email | Resend |
| Deployment | Vercel (web) + Railway (API) |

## Project Structure

```
coach-platform/
├── apps/
│   ├── web/          # Next.js frontend
│   └── api/          # Python FastAPI backend
├── supabase/         # Database migrations
├── packages/         # Shared code (future)
└── turbo.json        # Turborepo config
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.12+
- Supabase account
- Anthropic API key
- Resend API key

### 1. Clone and Install

```bash
git clone https://github.com/baby-benzing/coach-platform.git
cd coach-platform
npm install
```

### 2. Set Up Supabase

1. Create a new Supabase project at [supabase.com](https://supabase.com)
2. Run the migration in SQL Editor:
   - Copy contents of `supabase/migrations/20250101000000_initial_schema.sql`
   - Paste and run in Supabase SQL Editor
3. Get your credentials from Project Settings > API

### 3. Configure Environment Variables

**Frontend (`apps/web/.env.local`):**

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (`apps/api/.env`):**

```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_supabase_service_key
SUPABASE_JWT_SECRET=your_jwt_secret
ANTHROPIC_API_KEY=your_anthropic_api_key
RESEND_API_KEY=your_resend_api_key
FROM_EMAIL=noreply@yourdomain.com
CORS_ORIGINS=http://localhost:3000
```

### 4. Run Locally

**Terminal 1 - Backend:**

```bash
cd apps/api
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**

```bash
npm run dev:web
```

Open [http://localhost:3000](http://localhost:3000)

## Deployment

### Deploy Frontend to Vercel

1. Connect your GitHub repo to Vercel
2. Set root directory to `apps/web`
3. Add environment variables
4. Deploy

### Deploy Backend to Railway

1. Create new Railway project
2. Connect your GitHub repo
3. Set root directory to `apps/api`
4. Add environment variables
5. Deploy

### Update CORS

After deployment, update `CORS_ORIGINS` in Railway to include your Vercel URL.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/exercises` | GET, POST | List/create exercises |
| `/api/v1/exercises/{id}` | GET, PATCH, DELETE | Manage exercise |
| `/api/v1/clients` | GET, POST | List/create clients |
| `/api/v1/clients/{id}` | GET, PATCH, DELETE | Manage client |
| `/api/v1/clients/{id}/assessments` | GET, POST | Client assessments |
| `/api/v1/plans` | GET | List workout plans |
| `/api/v1/plans/{id}` | GET, PATCH | Manage plan |
| `/api/v1/plans/{id}/send-email` | POST | Email plan to client |

## Future Roadmap

- [ ] Mobile apps (iOS/Android) with React Native
- [ ] Full agentic workflow using Anthropic Agent SDK
- [ ] Real-time sync with Supabase Realtime
- [ ] Progress analytics and charts
- [ ] Video calling integration
- [ ] Payment processing

## License

MIT
