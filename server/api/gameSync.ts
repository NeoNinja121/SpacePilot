import express from 'express';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import path from 'path';

const router = express.Router();

// Ensure data directory exists
const dataDir = path.join(process.cwd(), 'data');
if (!existsSync(dataDir)) {
  mkdirSync(dataDir, { recursive: true });
}

// Path to the game stats file
const statsFilePath = path.join(dataDir, 'game_stats.json');

// Initialize stats file if it doesn't exist
if (!existsSync(statsFilePath)) {
  writeFileSync(
    statsFilePath,
    JSON.stringify({
      players: [],
      leaderboard: [],
      lastUpdated: new Date().toISOString(),
    }),
    'utf8'
  );
}

// Get game stats (for leaderboard)
router.get('/stats', (req: express.Request, res: express.Response) => {
  try {
    const statsData = readFileSync(statsFilePath, 'utf8');
    const stats = JSON.parse(statsData);
    res.json(stats);
  } catch (error) {
    console.error('Error reading stats file:', error);
    res.status(500).json({ error: 'Failed to read game stats' });
  }
});

// Update player stats
router.post('/sync', (req: express.Request, res: express.Response) => {
  try {
    const { playerId, playerName, distance, darkMatter, events } = req.body;
    
    if (!playerId || !playerName) {
      return res.status(400).json({ error: 'Player ID and name are required' });
    }
    
    // Read current stats
    const statsData = readFileSync(statsFilePath, 'utf8');
    const stats = JSON.parse(statsData);
    
    // Find or create player
    let playerIndex = stats.players.findIndex((p: any) => p.id === playerId);
    
    if (playerIndex === -1) {
      // New player
      stats.players.push({
        id: playerId,
        name: playerName,
        distance: distance || 0,
        darkMatter: darkMatter || 0,
        lastSync: new Date().toISOString(),
        significantEvents: events || [],
      });
    } else {
      // Update existing player
      stats.players[playerIndex] = {
        ...stats.players[playerIndex],
        name: playerName,
        distance: distance || stats.players[playerIndex].distance,
        darkMatter: darkMatter || stats.players[playerIndex].darkMatter,
        lastSync: new Date().toISOString(),
        significantEvents: events || stats.players[playerIndex].significantEvents,
      };
    }
    
    // Update leaderboard
    stats.leaderboard = stats.players
      .slice()
      .sort((a: any, b: any) => b.distance - a.distance)
      .slice(0, 100) // Top 100 players
      .map((player: any, index: number) => ({
        rank: index + 1,
        id: player.id,
        name: player.name,
        distance: player.distance,
      }));
    
    stats.lastUpdated = new Date().toISOString();
    
    // Save updated stats
    writeFileSync(statsFilePath, JSON.stringify(stats, null, 2), 'utf8');
    
    res.json({
      success: true,
      leaderboard: stats.leaderboard.slice(0, 10), // Send top 10 for display
    });
  } catch (error) {
    console.error('Error updating player stats:', error);
    res.status(500).json({ error: 'Failed to update player stats' });
  }
});

// Export the router
export default router;
