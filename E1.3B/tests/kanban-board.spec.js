const { test, expect } = require('@playwright/test');

test.describe('Tablero Kanban - Funcionalidad general', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
    await page.reload();
  });

  test.describe('Carga inicial', () => {
    test('muestra el título del tablero', async ({ page }) => {
      await expect(page.locator('.header h1')).toContainText('Tablero Kanban');
    });

    test('muestra 3 columnas', async ({ page }) => {
      const columns = page.locator('.column');
      await expect(columns).toHaveCount(3);
    });

    test('carga 6 tarjetas iniciales (2 por columna)', async ({ page }) => {
      await expect(page.locator('#col-todo .card')).toHaveCount(2);
      await expect(page.locator('#col-progress .card')).toHaveCount(2);
      await expect(page.locator('#col-done .card')).toHaveCount(2);
    });

    test('muestra los contadores correctos', async ({ page }) => {
      await expect(page.locator('#count-todo')).toHaveText('2');
      await expect(page.locator('#count-progress')).toHaveText('2');
      await expect(page.locator('#count-done')).toHaveText('2');
    });

    test('las tarjetas iniciales tienen los títulos esperados', async ({ page }) => {
      const titles = await page.locator('.card-title').allTextContents();
      expect(titles).toContain('Configurar ESLint');
      expect(titles).toContain('Diseñar API REST');
      expect(titles).toContain('Implementar login');
      expect(titles).toContain('Crear tests unitarios');
      expect(titles).toContain('Setup del repositorio');
      expect(titles).toContain('Documentar README');
    });
  });

  test.describe('Añadir tarjeta', () => {
    test('abre y cierra el modal de nueva tarjeta', async ({ page }) => {
      const overlay = page.locator('#form-overlay');
      await expect(overlay).not.toHaveClass(/active/);

      await page.click('#btn-add');
      await expect(overlay).toHaveClass(/active/);

      await page.click('#btn-cancel');
      await expect(overlay).not.toHaveClass(/active/);
    });

    test('crea una nueva tarjeta en "Por Hacer"', async ({ page }) => {
      await page.click('#btn-add');
      await page.fill('#input-title', 'Nueva tarea de prueba');
      await page.fill('#input-desc', 'Descripción de prueba');
      await page.selectOption('#input-priority', 'alta');
      await page.click('button[type="submit"]');

      await expect(page.locator('#col-todo .card')).toHaveCount(3);
      await expect(page.locator('#col-todo .card-title').last()).toHaveText('Nueva tarea de prueba');
    });

    test('no permite crear tarjeta sin título', async ({ page }) => {
      await page.click('#btn-add');
      // El input tiene atributo "required", así que el formulario no se envía
      const input = page.locator('#input-title');
      await expect(input).toHaveAttribute('required', '');

      // Intentar submit con título vacío no crea tarjeta
      await page.click('button[type="submit"]');
      await expect(page.locator('#col-todo .card')).toHaveCount(2);
    });

    test('la tarjeta creada persiste tras recargar', async ({ page }) => {
      await page.click('#btn-add');
      await page.fill('#input-title', 'Tarea persistente');
      await page.click('button[type="submit"]');

      await page.reload();

      const titles = await page.locator('.card-title').allTextContents();
      expect(titles).toContain('Tarea persistente');
    });
  });

  test.describe('Editar título inline', () => {
    test('permite editar título con doble clic', async ({ page }) => {
      const firstTitle = page.locator('.card-title').first();
      const originalText = await firstTitle.textContent();

      await firstTitle.dblclick();

      const input = page.locator('.card-title-input');
      await expect(input).toBeVisible();
      await expect(input).toHaveValue(originalText);

      await input.fill('Título editado');
      await input.press('Enter');

      await expect(page.locator('.card-title').first()).toHaveText('Título editado');
    });

    test('la edición de título persiste tras recargar', async ({ page }) => {
      const firstTitle = page.locator('.card-title').first();
      await firstTitle.dblclick();

      const input = page.locator('.card-title-input');
      await input.fill('Título persistente editado');
      await input.press('Enter');

      await page.reload();

      const titles = await page.locator('.card-title').allTextContents();
      expect(titles).toContain('Título persistente editado');
    });

    test('cancelar edición con Escape restaura el título original', async ({ page }) => {
      const firstTitle = page.locator('.card-title').first();
      const originalText = await firstTitle.textContent();

      await firstTitle.dblclick();
      const input = page.locator('.card-title-input');
      await input.fill('Texto que no se guarda');
      await input.press('Escape');

      await expect(page.locator('.card-title').first()).toHaveText(originalText);
    });
  });

  test.describe('Eliminar tarjeta', () => {
    test('requiere doble clic para eliminar (confirmación)', async ({ page }) => {
      const initialCount = await page.locator('.card').count();
      const deleteBtn = page.locator('.card-delete').first();

      // Primer clic: activa confirmación
      await deleteBtn.click({ force: true });
      await expect(deleteBtn).toHaveClass(/confirm/);

      // Segundo clic: elimina
      await deleteBtn.click({ force: true });

      await expect(page.locator('.card')).toHaveCount(initialCount - 1);
    });

    test('la eliminación persiste tras recargar', async ({ page }) => {
      const deleteBtn = page.locator('.card-delete').first();
      await deleteBtn.click({ force: true });
      await deleteBtn.click({ force: true });

      const countAfterDelete = await page.locator('.card').count();
      await page.reload();

      await expect(page.locator('.card')).toHaveCount(countAfterDelete);
    });
  });

  test.describe('Filtro de prioridad', () => {
    test('filtrar por "Alta" muestra solo tarjetas de prioridad alta', async ({ page }) => {
      await page.selectOption('#filter', 'alta');

      const visible = page.locator('.card:not(.hidden)');
      const badges = await visible.locator('.badge').allTextContents();

      expect(badges.length).toBeGreaterThan(0);
      for (const b of badges) {
        expect(b.trim()).toBe('alta');
      }
    });

    test('filtrar por "Todas" muestra todas las tarjetas', async ({ page }) => {
      await page.selectOption('#filter', 'alta');
      await page.selectOption('#filter', 'todas');

      const hidden = page.locator('.card.hidden');
      await expect(hidden).toHaveCount(0);
    });

    test('los contadores se actualizan según el filtro', async ({ page }) => {
      await page.selectOption('#filter', 'baja');

      const todoCount = await page.locator('#count-todo').textContent();
      const progressCount = await page.locator('#count-progress').textContent();
      const doneCount = await page.locator('#count-done').textContent();
      const total = parseInt(todoCount) + parseInt(progressCount) + parseInt(doneCount);

      // Solo hay 2 tarjetas de prioridad baja en datos iniciales
      expect(total).toBe(2);
    });
  });

  test.describe('Reiniciar tablero', () => {
    test('reiniciar restaura las 6 tarjetas iniciales', async ({ page }) => {
      // Añadir una tarjeta extra
      await page.click('#btn-add');
      await page.fill('#input-title', 'Tarjeta extra');
      await page.click('button[type="submit"]');
      await expect(page.locator('.card')).toHaveCount(7);

      // Reiniciar
      page.on('dialog', dialog => dialog.accept());
      await page.click('#btn-reset');

      await expect(page.locator('.card')).toHaveCount(6);
    });

    test('cancelar reinicio no borra las tarjetas', async ({ page }) => {
      page.on('dialog', dialog => dialog.dismiss());
      await page.click('#btn-reset');

      await expect(page.locator('.card')).toHaveCount(6);
    });
  });

  test.describe('Modal del formulario', () => {
    test('cerrar modal con Escape', async ({ page }) => {
      await page.click('#btn-add');
      await expect(page.locator('#form-overlay')).toHaveClass(/active/);

      await page.keyboard.press('Escape');
      await expect(page.locator('#form-overlay')).not.toHaveClass(/active/);
    });

    test('cerrar modal al hacer clic en el overlay', async ({ page }) => {
      await page.click('#btn-add');
      await expect(page.locator('#form-overlay')).toHaveClass(/active/);

      // Clic en el overlay (fuera del formulario)
      await page.locator('#form-overlay').click({ position: { x: 10, y: 10 } });
      await expect(page.locator('#form-overlay')).not.toHaveClass(/active/);
    });
  });
});
