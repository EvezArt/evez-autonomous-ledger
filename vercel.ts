import type { VercelConfig } from '@vercel/config/v1';

export const config: VercelConfig = {
  framework: 'nextjs',
  buildCommand: 'next build',
  github: {
    autoJobCancelation: false,
  },
  crons: [
    {
      path: '/api/crons/provider-health',
      schedule: '*/2 * * * *',
    },
    {
      path: '/api/crons/route-precompute',
      schedule: '*/5 * * * *',
    },
  ],
};
