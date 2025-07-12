

export const metadataKeyMap: Record<string, string> = {
  'start-index-nbr': 'Start Index',
  'end-index-nbr': 'End Index',
  'row_adder-cnt': 'Row Adder Count',
  'col_adder_cnt': 'Column Adder Count',
  'param-ref_delim_txt': 'Parameter Delimiter',
  'param_value_pos_cd': 'Parameter Value Position Code',
  'unit_price_pct_ind': 'Unit Price Percent Indicator',
  'param_nm_occur_ind': 'Parameter Occurrence Indicator',
  'date_format_cd': 'Date Format Code',
  'decimal_seperator_cd': 'Decimal Separator Code',
  'param_def_value_txt': 'Parameter Default Value',
  'derivation_col': 'Derivation Column',
  'operations_seq': 'Operations Sequence',
  'param_val_fn_txt': 'Parameter Value Text'
};


export function mapMetadataKeys(
  metadata: Record<string, any>,
  keyMap: Record<string, string> = metadataKeyMap
): Record<string, any> {
  const newMetadata: Record<string, any> = {};
  for (const key in metadata) {
    const newKey = keyMap[key] || key;
    newMetadata[newKey] = metadata[key];
  }
  return newMetadata;
}
