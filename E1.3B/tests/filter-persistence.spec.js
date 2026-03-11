const { test, expect } = require('@playwright/test');

test.describe('Persistencia del filtro de prioridad', () => {
  test.beforeEach(async ({ page }) => {
    // Limpiar localStorage antes de cada test
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
    await page.reload();
  });

  test('el filtro inicia en "Todas" por defecto', async ({ page }) => {
    const filter = page.locator('#filter');
    await expect(filter).toHaveValue('todas');
  });

  test('el filtro seleccionado se guarda en localStorage', async ({ page }) => {
    const filter = page.locator('#filter');

    await filter.selectOption('alta');

    const savedFilter = await page.evaluate(() => localStorage.getItem('kanban-filter'));
    expect(savedFilter).toBe('alta');
  });

  test('el filtro persiste tras recargar la página', async ({ page }) => {
    const filter = page.locator('#filter');

    await filter.selectOption('media');
    await page.reload();

    await expect(filter).toHaveValue('media');
  });

  test('el filtro persiste con cada opción disponible', async ({ page }) => {
    const filter = page.locator('#filter');

    for (const value of ['alta', 'media', 'baja', 'todas']) {
      await filter.selectOption(value);
      await page.reload();
      await expect(filter).toHaveValue(value);
    }
  });

  test('el filtro se limpia al reiniciar el tablero', async ({ page }) => {
    const filter = page.locator('#filter');

    await filter.selectOption('baja');
    // Verificar que se guardó
    const saved = await page.evaluate(() => localStorage.getItem('kanban-filter'));
    expect(saved).toBe('baja');

    // Reiniciar tablero (aceptar confirmación)
    page.on('dialog', dialog => dialog.accept());
    await page.click('#btn-reset');

    await expect(filter).toHaveValue('todas');

    const clearedFilter = await page.evaluate(() => localStorage.getItem('kanban-filter'));
    expect(clearedFilter).toBeNull();
  });

  test('las tarjetas se filtran correctamente según el filtro persistido', async ({ page }) => {
    const filter = page.locator('#filter');

    await filter.selectOption('alta');
    await page.reload();

    // Solo deben verse tarjetas con prioridad alta
    const visibleCards = page.locator('.card:not(.hidden)');
    const hiddenCards = page.locator('.card.hidden');

    await expect(visibleCards).not.toHaveCount(0);
    await expect(hiddenCards).not.toHaveCount(0);

    // Verificar que todas las visibles son de prioridad alta
    const badges = await visibleCards.locator('.badge').allTextContents();
    for (const badge of badges) {
      expect(badge.trim()).toBe('alta');
    }
  });

  test('un valor inválido en localStorage no rompe la app', async ({ page }) => {
    await page.evaluate(() => localStorage.setItem('kanban-filter', 'invalido'));
    await page.reload();

    const filter = page.locator('#filter');
    // Debe quedar en el valor por defecto
    await expect(filter).toHaveValue('todas');
  });
});
