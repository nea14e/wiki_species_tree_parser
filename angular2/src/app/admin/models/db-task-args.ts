export class DbTaskArgs {
  list_page_title!: string;
  from_title!: string;
  skip_parsed_interval = true;
  where!: string;
  lang_key!: string;
  proxy!: string;
  timeout = 35;
  will_success = true;
}
