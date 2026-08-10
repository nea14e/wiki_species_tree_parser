export class Right {
  constructor(public r: string) {
  }
}

export const RIGHTS = {
  SUPER_ADMIN: new Right('[SUPER_ADMIN]'),  // фиктивное право, которое есть только у суперадмина и выдать никому его нельзя
  EDIT_DB_TASKS: new Right('[EDIT_DB_TASKS]'),
  EDIT_LANGUAGES_LIST: new Right('[EDIT_LANGUAGES_LIST]'),
  EDIT_TIPS_LIST: new Right('[EDIT_TIPS_LIST]'),
};  // Кроме того, есть права переводить на каждый из языков
