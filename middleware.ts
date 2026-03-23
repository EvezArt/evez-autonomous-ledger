import { NextResponse } from 'next/server';
import { get } from '@vercel/edge-config';

export const config = {
  matcher: ['/api/run', '/api/resume'],
  runtime: 'nodejs',
};

export default async function middleware(req: Request) {
  const mode = await get('defaultOperatingMode');
  const headers = new Headers(req.headers);

  if (mode) headers.set('x-operator-mode', String(mode));

  return NextResponse.next({
    request: { headers },
  });
}
