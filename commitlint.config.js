module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        // Standard types
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation changes
        'chore',    // Maintenance tasks
        'refactor', // Code refactoring
        'test',     // Testing changes
        'style',    // Code style changes
        'perf',     // Performance improvements
        'ci',       // CI/CD changes
        'build',    // Build system changes
        'revert',   // Revert previous commit

        // Hardware-specific types
        'hw',       // General hardware changes
        'pcb',      // PCB layout changes
        'sch',      // Schematic changes
        'bom',      // Bill of Materials updates
        'gerber',   // Gerber file generation
        'design',   // Design rule or constraint changes
        'lib',      // Component library updates
      ],
    ],
    'subject-case': [2, 'never', ['upper-case']],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'type-case': [2, 'always', 'lower-case'],
    'type-empty': [2, 'never'],
  },
};
