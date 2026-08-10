export class DbTaskArgs {
  from_title!: string;
  to_title!: string;
  skip_parsed_interval = true;
  where!: string;
  lang_key!: string;
  proxy!: string;
  timeout = 35;
  will_success = true;
}
