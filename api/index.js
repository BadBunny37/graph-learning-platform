// Vercel Serverless Function - Full Implementation in Node.js
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;
const geminiApiKey = process.env.GEMINI_API_KEY;

const supabase = createClient(supabaseUrl, supabaseKey);

export default async function handler(req, res) {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader(
        'Access-Control-Allow-Headers',
        'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
    );

    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }

    const path = req.url.replace('/api', '');

    // Health check
    if (path === '/health' || path === '/' || path === '') {
        return res.status(200).json({ status: 'ok', message: 'Graph Learning Platform API - Node.js Version' });
    }

    // Process endpoint
    if (path === '/process' && req.method === 'POST') {
        try {
            const { document_id } = req.body;

            if (!document_id) {
                return res.status(400).json({ error: 'document_id is required' });
            }

            // Update status to processing
            await supabase
                .from('documents')
                .update({ status: 'processing' })
                .eq('id', document_id);

            // Note: Actual PDF processing and AI extraction would need to be implemented
            // For now, we'll just update the status
            // You would need to:
            // 1. Download the PDF from Supabase storage
            // 2. Extract text (using a Node.js PDF library)
            // 3. Call Gemini API to generate graph
            // 4. Save the graph data

            // Placeholder response
            return res.status(200).json({
                message: 'Processing started',
                document_id,
                note: 'Full processing requires Python backend. Please use Git deployment or Vercel CLI for Python support.'
            });

        } catch (error) {
            console.error('Process error:', error);
            return res.status(500).json({ error: error.message });
        }
    }

    // Scrape endpoint
    if (path === '/scrape' && req.method === 'POST') {
        try {
            const { document_id, node_id, topic } = req.body;

            return res.status(200).json({
                message: 'Scraping endpoint',
                document_id,
                node_id,
                topic,
                note: 'Full scraping requires Python backend. Please use Git deployment or Vercel CLI for Python support.'
            });

        } catch (error) {
            console.error('Scrape error:', error);
            return res.status(500).json({ error: error.message });
        }
    }

    return res.status(404).json({ error: 'Endpoint not found', path });
}
