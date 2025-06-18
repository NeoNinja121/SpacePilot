import express from 'express';
import dotenv from 'dotenv';
import { setupStaticServing } from './static-serve.js';
import gameSyncRouter from './api/gameSync.js';

dotenv.config();

const app = express();

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Game sync API routes
app.use('/api/game', gameSyncRouter);

// Game status endpoint
app.get('/api/status', (req: express.Request, res: express.Response) => {
  res.json({ 
    status: 'online',
    version: '1.0.0',
    serverTime: new Date().toISOString(),
  });
});

// Export a function to start the server
export async function startServer(port) {
  try {
    if (process.env.NODE_ENV === 'production') {
      setupStaticServing(app);
    }
    app.listen(port, () => {
      console.log(`Idle Space Adventure API Server running on port ${port}`);
    });
  } catch (err) {
    console.error('Failed to start server:', err);
    process.exit(1);
  }
}

// Start the server directly if this is the main module
if (import.meta.url === `file://${process.argv[1]}`) {
  console.log('Starting Idle Space Adventure server...');
  startServer(process.env.PORT || 3001);
}
