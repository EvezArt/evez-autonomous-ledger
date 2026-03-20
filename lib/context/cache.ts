import { getCache } from '@vercel/functions';

const cache = getCache({ namespace: 'evez-operator' });

export async function getHotContext(key: string) {
  return cache.get(`ctx:${key}`);
}

export async function setHotContext(key: string, value: unknown, ttl = 900) {
  await cache.set(`ctx:${key}`, value, {
    ttl,
    tags: ['context'],
  });
}

export async function getHotRoute(key: string) {
  return cache.get(`route:${key}`);
}

export async function setHotRoute(key: string, value: unknown, ttl = 300) {
  await cache.set(`route:${key}`, value, {
    ttl,
    tags: ['route'],
  });
}
